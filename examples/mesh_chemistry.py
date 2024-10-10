"""Example building MESH 2024 dataset."""

import argparse
import networkx as nx
from mesh.settings import DatasetSettings, ChemicalsAndDrugsSettings
from mesh import Dataset


def build_mesh_chemistry(
    year: int,
) -> Dataset:
    """Build MESH dataset."""
    # First, we need to define the settings for the dataset.
    cad: ChemicalsAndDrugsSettings = (
        ChemicalsAndDrugsSettings()
        # In this case, we are including all of the submodules of
        # categories of chemicals and drugs.
        .include_all_submodules()
        # We also want to include SMILES, which we obtain from the
        # PUBCHEM database.
        .include_smiles()
        # Analogously, we want to include InChI keys, which we obtain
        # from the PUBCHEM database.
        .include_inchi_keys()
    )
    settings = (
        # We are using the MESH 2024 version.
        DatasetSettings(version=year)
        # We want to retrieve data only regarding chemicals and drugs.
        .include_chemicals_and_drugs(cad)
        # And we want to print the progress of the dataset retrieval.
        .set_verbose(True)
    )
    # Now, we build the dataset. This will download the necessary files
    # and rasterize the dataset.
    dataset = Dataset.build(settings)
    return dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build MESH dataset.")
    parser.add_argument(
        "--year",
        type=int,
        default=2024,
        help="Year of the MESH dataset.",
    )
    parser.add_argument(
        "--tarball",
        action="store_true",
        help="Whether to save the dataset as a tarball.",
    )
    args = parser.parse_args()

    # We build the MESH  dataset.
    mesh_chemistry: Dataset = build_mesh_chemistry(args.year)
    # And we save it to disk.
    mesh_chemistry.save(f"mesh_{args.year}", tarball=args.tarball)

    # We convert the MESH dataset to a NetworkX graph.
    graph: nx.DiGraph = mesh_chemistry.to_networkx()

    # Now, we can use the NetworkX graph as we would any other NetworkX graph.
    print(graph)
