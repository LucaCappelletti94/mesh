"""Submodule providing a Compound ID enricher for the MESH dataset."""

from typing import Any, Dict
import os
from tqdm.auto import tqdm
from downloaders import BaseDownloader
from mesh.enrichers.enricher import Enricher
from mesh.utils import MaybeChemical


class CompoundIdEnricher(Enricher):
    """Enricher for the Compound ID field."""

    def __init__(
        self,
        downloads_directory: str,
        verbose: bool = False,
    ):
        """Initialize the enricher."""
        cid_path = os.path.join(downloads_directory, "CID-MeSH.txt")
        sid_path = os.path.join(downloads_directory, "SID-MeSH.txt")

        BaseDownloader(
            process_number=1,
            verbose=verbose,
        ).download(
            [
                "https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-MeSH",
                "https://ftp.ncbi.nlm.nih.gov/pubchem/Substance/Extras/SID-MeSH",
            ],
            [
                cid_path,
                sid_path,
            ],
        )

        loading_bar = tqdm(
            desc="Loading Compound ID mappings",
            disable=not verbose,
            leave=False,
            dynamic_ncols=True,
        )

        self._compound_id_to_mesh: Dict[str, int] = {}

        with open(cid_path, "r", encoding="utf-8") as file:
            for line in file:
                mappings = line.strip().split("\t")
                compound_id = mappings[0]
                mesh_compounds = mappings[1:]
                for mesh_compound in mesh_compounds:
                    self._compound_id_to_mesh[mesh_compound] = int(compound_id)
                    loading_bar.update(1)

        loading_bar.close()

        loading_bar = tqdm(
            desc="Loading Substance ID mappings",
            disable=not verbose,
            leave=False,
            dynamic_ncols=True,
        )

        self._substance_id_to_mesh: Dict[str, int] = {}

        with open(sid_path, "r", encoding="utf-8") as file:
            for line in file:
                mappings = line.strip().split("\t")
                substance_id = mappings[0]
                mesh_compounds = mappings[1:]
                for mesh_compound in mesh_compounds:
                    self._substance_id_to_mesh[mesh_compound] = int(substance_id)
                    loading_bar.update(1)

        loading_bar.close()

    def name(self):
        """Return the name of the enricher."""
        return "Compound ID"

    def enrich(self, entry: Any):
        """Enrich the row with the Compound ID field."""
        if not isinstance(entry, MaybeChemical):
            return

        if not entry.maybe_chemical():
            return

        chemical_name: str = entry.chemical_name()
        compound_id: int = self._compound_id_to_mesh.get(chemical_name, None)
        substance_id: int = self._substance_id_to_mesh.get(chemical_name, None)

        if compound_id is not None:
            entry.set_compound_id(compound_id)

        if substance_id is not None:
            entry.set_substance_id(substance_id)
