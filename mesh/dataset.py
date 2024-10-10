"""Submodule providing the Dataset class, representing an instance of the MESH dataset."""

from typing import List, Dict, Set
import os
import shutil
import pandas as pd
import compress_json
from downloaders import BaseDownloader
from tqdm.auto import tqdm
import networkx as nx
from mesh.settings import DatasetSettings
from mesh.descriptors_reader import MESHDescriptorsReader, MESHDescriptor
from mesh.chemicals_reader import MESHChemicalsReader, MESHChemical


class Dataset:
    """Class representing a MESH dataset."""

    def __init__(
        self,
        chemicals: pd.DataFrame,
        descriptors: pd.DataFrame,
        chemicals_to_descriptors: pd.DataFrame,
        mesh_dag: pd.DataFrame,
        metadata: Dict,
    ):
        """Initialize the Dataset class."""
        self._chemicals: pd.DataFrame = chemicals
        self._descriptors: pd.DataFrame = descriptors
        self._chemicals_to_descriptors: pd.DataFrame = chemicals_to_descriptors
        self._mesh_dag: pd.DataFrame = mesh_dag
        self._metadata: Dict = metadata

    def save(self, path: str, tarball: bool = False) -> None:
        """Save the dataset to disk."""
        os.makedirs(path, exist_ok=True)
        self._chemicals.to_csv(os.path.join(path, "chemicals.csv"), index=False)
        self._descriptors.to_csv(os.path.join(path, "descriptors.csv"), index=False)
        self._chemicals_to_descriptors.to_csv(
            os.path.join(path, "chemicals_to_descriptors.csv"), index=False
        )
        self._mesh_dag.to_csv(os.path.join(path, "mesh_dag.csv"), index=False)
        compress_json.dump(self._metadata, os.path.join(path, "metadata.json"))

        if tarball:
            os.system(f"tar -czf {path}.tar.gz {path}")
            shutil.rmtree(path)

    def to_networkx(self) -> nx.DiGraph:
        """Return the dataset as a networkx graph."""
        graph = nx.DiGraph()

        for _, row in self._chemicals.iterrows():
            graph.add_node(row["unique_identifier"], **row.to_dict())

        for _, row in self._descriptors.iterrows():
            graph.add_node(row["unique_identifier"], **row.to_dict())

        for _, row in self._chemicals_to_descriptors.iterrows():
            graph.add_edge(row["chemical"], row["descriptor"])

        for _, row in self._mesh_dag.iterrows():
            graph.add_edge(row["child"], row["parent"])

        return graph

    @staticmethod
    def load(
        version: str,
        download_directory: str = "downloads",
        verbose: bool = True,
    ) -> "Dataset":
        """Load the dataset from disk."""
        preprocessed: List[Dict[str, str]] = compress_json.local_load(
            "preprocessed.json"
        )

        version_metadata: Dict[str, str] = None

        for metadata in preprocessed:
            if metadata["version"] == version:
                version_metadata = metadata
                break

        if version_metadata is None:
            raise ValueError(
                f"Version {version} not found. "
                f"Available versions are {[metadata['version'] for metadata in preprocessed]}."
            )

        BaseDownloader(
            verbose=verbose,
        ).download(
            urls=[version_metadata["url"]],
            paths=[os.path.join(download_directory, f"{version}.tar.gz")],
        )

        chemicals = pd.read_csv(
            os.path.join(download_directory, version, "chemicals.csv")
        )
        descriptors = pd.read_csv(
            os.path.join(download_directory, version, "descriptors.csv")
        )
        chemicals_to_descriptors = pd.read_csv(
            os.path.join(download_directory, version, "chemicals_to_descriptors.csv")
        )
        mesh_dag = pd.read_csv(
            os.path.join(download_directory, version, "mesh_dag.csv")
        )
        metadata = compress_json.load(
            os.path.join(download_directory, version, "metadata.json")
        )

        return Dataset(
            chemicals=chemicals,
            descriptors=descriptors,
            chemicals_to_descriptors=chemicals_to_descriptors,
            mesh_dag=mesh_dag,
            metadata=metadata,
        )

    @staticmethod
    def build(settings: DatasetSettings) -> "Dataset":
        """Rasterize the dataset."""
        assert isinstance(settings, DatasetSettings)
        downloader = BaseDownloader(
            process_number=1,
            verbose=settings.verbose,
        )
        paths: List[str] = []
        urls: List[str] = []

        for download_objective in settings.download_objectives():
            paths.append(
                os.path.join(
                    settings.downloads_directory,
                    download_objective.path,
                )
            )
            urls.append(download_objective.url)

        downloader.download(urls=urls, paths=paths)

        descriptors: List[MESHDescriptor] = list(
            MESHDescriptorsReader(settings=settings)
        )

        chemicals: List[MESHChemical] = list(MESHChemicalsReader(settings=settings))

        enrichment_procedures = settings.enrichment_procedures()

        for enricher in tqdm(
            enrichment_procedures,
            desc="Enriching dataset",
            disable=not settings.verbose,
            leave=False,
            dynamic_ncols=True,
        ):
            for descriptor in descriptors:
                enricher.enrich(entry=descriptor)
            for chemical in chemicals:
                enricher.enrich(entry=chemical)

        # We construct the edges of the graph
        chemical_sources: List[str] = []
        descriptor_destinations: List[str] = []
        descriptors_unique_ids = {
            descriptor.unique_identifier for descriptor in descriptors
        }
        for chemical in tqdm(
            chemicals,
            desc="Constructing chemical to descriptor edges",
            disable=not settings.verbose,
            leave=False,
            dynamic_ncols=True,
        ):
            for descriptors_unique_id in chemical.descriptors:
                # The user may have configured this Dataset to some descriptors.
                if descriptors_unique_id in descriptors_unique_ids:
                    chemical_sources.append(chemical.unique_identifier)
                    descriptor_destinations.append(descriptors_unique_id)

            for pharmacological_actions_unique_id in chemical.pharmacological_actions:
                # The user may have configured this Dataset to exclude pharmacological actions.
                if pharmacological_actions_unique_id in descriptors_unique_ids:
                    chemical_sources.append(chemical.unique_identifier)
                    descriptor_destinations.append(pharmacological_actions_unique_id)

        chemicals_to_descriptors = pd.DataFrame(
            {
                "chemical": chemical_sources,
                "descriptor": descriptor_destinations,
            }
        )

        descriptors_sources: List[str] = []
        descriptors_destinations: List[str] = []

        mesh_dag_numbers = {}
        for descriptor in tqdm(
            descriptors,
            desc="Constructing mesh tree numbers lookup",
            disable=not settings.verbose,
            leave=False,
            dynamic_ncols=True,
        ):
            for tree_number in descriptor.mesh_dag_numbers():
                mesh_dag_numbers[".".join(tree_number)] = descriptor.unique_identifier

        for descriptor in tqdm(
            descriptors,
            desc="Constructing MESH DAG edges",
            disable=not settings.verbose,
            leave=False,
            dynamic_ncols=True,
        ):
            # In some instances, the parent tree number in MESH
            # since it treats it as a path on a tree from the root to the leaf,
            # while here we are treating it as a graph.
            parents: Set[str] = set()
            for tree_number in descriptor.mesh_dag_numbers():
                if len(tree_number) == 1:
                    # Skip the root node.
                    continue
                tree_number = ".".join(tree_number[:-1])
                assert (
                    tree_number in mesh_dag_numbers
                ), f"Tree number {tree_number} not found in descriptors."
                destination = mesh_dag_numbers[tree_number]

                if destination in parents:
                    continue

                parents.add(destination)

                assert (
                    destination != descriptor.unique_identifier
                ), f"Cycle detected: {descriptor.unique_identifier} -> {destination}"
                descriptors_sources.append(descriptor.unique_identifier)
                descriptors_destinations.append(destination)

        mesh_dag = pd.DataFrame(
            {
                "child": descriptors_sources,
                "parent": descriptors_destinations,
            }
        )

        # Next, we construct the node lists.

        chemicals_df = pd.DataFrame([chemical.into_dict() for chemical in chemicals])

        descriptors_df = pd.DataFrame(
            [descriptor.into_dict() for descriptor in descriptors]
        )

        return Dataset(
            chemicals=chemicals_df,
            descriptors=descriptors_df,
            chemicals_to_descriptors=chemicals_to_descriptors,
            mesh_dag=mesh_dag,
            metadata=settings.into_dict(),
        )
