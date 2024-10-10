"""Submodule representing a Chemical in the MESH dataset."""

from typing import List


class Chemical:

    @property
    def name(self) -> str:
        """Return the name of the molecule."""
        return ""

    @property
    def pharmacological_actions(self) -> List[str]:
        """Return a list of pharmacological actions."""
        return []

    @property
    def cid(self) -> int:
        """Return the PubChem Compound ID."""
        return 0

    @property
    def smiles(self) -> str:
        """Return the SMILES string."""
        return ""

    @property
    def inchikey(self) -> str:
        """Return the InChIKey."""
        return ""
