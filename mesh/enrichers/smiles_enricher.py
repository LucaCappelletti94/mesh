"""Submodule providing a SMILES enricher for the MESH dataset."""

from typing import Any
import os
from tqdm.auto import tqdm
from downloaders import BaseDownloader
from mesh.enrichers.enricher import Enricher
from mesh.utils import MaybeChemical


class SMILESEnricher(Enricher):
    """Enricher for the SMILES field."""

    def __init__(
        self,
        downloads_directory: str,
        verbose: bool = False,
    ):
        """Initialize the enricher."""
        path = os.path.join(downloads_directory, "CID-SMILES.tsv.gz")
        extracted_path = os.path.join(downloads_directory, "CID-SMILES.tsv")
        BaseDownloader(
            process_number=1,
            verbose=verbose,
        ).download(
            "https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-SMILES.gz",
            path,
        )

        loading_bar = tqdm(
            desc="Extracting SMILES",
            disable=not verbose,
            leave=False,
            dynamic_ncols=True,
        )

        self._compound_id_to_smiles = {}

        with open(extracted_path, "r", encoding="utf-8") as file:
            for line in file:
                compound_id, smiles = line.strip().split("\t")
                self._compound_id_to_smiles[int(compound_id)] = smiles
                loading_bar.update(1)

        loading_bar.close()

    def name(self):
        """Return the name of the enricher."""
        return "SMILES"

    def enrich(self, entry: Any):
        """Enrich the row with the SMILES field."""
        if not isinstance(entry, MaybeChemical):
            return

        if entry.compound_id() is None:
            return

        smiles: str = self._compound_id_to_smiles.get(entry.compound_id(), None)

        if smiles is not None:
            entry.set_smiles(smiles)
