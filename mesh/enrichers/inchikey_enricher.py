"""Submodule providing a InChIKey enricher for the MESH dataset."""

from typing import Any, Dict, Tuple
import os
from tqdm.auto import tqdm
from downloaders import BaseDownloader
from mesh.enrichers.enricher import Enricher
from mesh.utils import MaybeChemical


class InChIKeyEnricher(Enricher):
    """Enricher for the InChIKey field."""

    def __init__(
        self,
        downloads_directory: str,
        verbose: bool = False,
    ):
        """Initialize the enricher."""
        path = os.path.join(downloads_directory, "CID-InChIKey.tsv.gz")
        extracted_path = os.path.join(downloads_directory, "CID-InChIKey.tsv")
        BaseDownloader(
            process_number=1,
            verbose=verbose,
        ).download(
            "https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-InChI-Key.gz",
            path,
        )

        loading_bar = tqdm(
            desc="Extracting InChIKey",
            disable=not verbose,
            leave=False,
            dynamic_ncols=True,
        )

        self._compound_id_to_inchi: Dict[int, Tuple[str, str]] = {}

        with open(extracted_path, "r", encoding="utf-8") as file:
            for line in file:
                compound_id, inchi, inchikey = line.strip().split("\t")
                self._compound_id_to_inchi[int(compound_id)] = (inchi, inchikey)
                loading_bar.update(1)

        loading_bar.close()

    def name(self):
        """Return the name of the enricher."""
        return "InChIKey"

    def enrich(self, entry: Any):
        """Enrich the row with the InChIKey field."""
        if not isinstance(entry, MaybeChemical):
            return

        if entry.compound_id() is None:
            return

        (inchi, inchikey) = self._compound_id_to_inchi.get(entry.compound_id(), (None, None))

        if inchi is not None:
            entry.set_inchi_and_inchikey(inchi, inchikey)
