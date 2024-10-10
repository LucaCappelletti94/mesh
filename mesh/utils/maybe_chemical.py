"""Submodule providing the MaybeChemical interface to model objects that at times are chemicals."""

from abc import ABC, abstractmethod
from typing import Optional


class MaybeChemical(ABC):
    """Interface for objects that at times are chemicals."""

    @abstractmethod
    def maybe_chemical(self) -> bool:
        """Return True if the object is a chemical."""

    @abstractmethod
    def chemical_name(self) -> str:
        """Return the name of the chemical."""

    @abstractmethod
    def compound_id(self) -> Optional[int]:
        """Return the PubChem Compound ID of the chemical."""

    @abstractmethod
    def set_compound_id(self, compound_id: int) -> None:
        """Set the PubChem Compound ID of the chemical."""

    @abstractmethod
    def substance_id(self) -> Optional[int]:
        """Return the PubChem Substance ID of the chemical."""

    @abstractmethod
    def set_substance_id(self, substance_id: int) -> None:
        """Set the PubChem Substance ID of the chemical."""

    @abstractmethod
    def smiles(self) -> Optional[str]:
        """Return the SMILES string of the chemical."""

    @abstractmethod
    def set_smiles(self, smiles: str) -> None:
        """Set the SMILES string of the chemical."""

    @abstractmethod
    def inchikey(self) -> Optional[str]:
        """Return the InChIKey of the chemical."""

    @abstractmethod
    def set_inchikey(self, inchikey: str) -> None:
        """Set the InChIKey of the chemical."""
