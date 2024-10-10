"""Submodule providing a reader able to read the MESH descriptors."""

import os
from typing import Iterator, List, Optional
from mesh.reader import MESHReader
from mesh.settings import DatasetSettings
from mesh.utils import normalize_string, MaybeChemical


class MESHDescriptor(MaybeChemical):
    """Class representing a MESH descriptor."""

    def __init__(
        self, name: str, unique_identifier: str, mesh_tree_numbers: List[List[str]]
    ):
        """Initialize the MESHDescriptor class."""
        self._name: str = name
        self._unique_identifier: str = unique_identifier
        self._mesh_tree_numbers: List[List[str]] = mesh_tree_numbers
        self._compound_id: Optional[int] = None
        self._substance_id: Optional[int] = None
        self._smiles: Optional[str] = None
        self._inchikey: Optional[str] = None

    def __repr__(self) -> str:
        """Return the representation of the MESH descriptor."""
        return f"MESHDescriptor(name='{self._name}', tree_numbers={self._mesh_tree_numbers}, compound_id={self._compound_id}, substance_id={self._substance_id}, smiles={self._smiles}, inchikey={self._inchikey})"

    def mesh_tree_numbers(self) -> List[List[str]]:
        """Return the MESH tree numbers."""
        return self._mesh_tree_numbers

    def has_mesh_tree_numbers(self) -> bool:
        """Return whether the descriptor has mesh tree numbers."""
        return len(self._mesh_tree_numbers) > 0

    def chemical_name(self) -> str:
        """Return the name of the descriptor."""
        return self._name

    def maybe_chemical(self) -> bool:
        """Return whether the descriptor is a chemical."""
        haystack = [
            "D01",
            "D02",
            "D03",
            "D04",
            "D05",
            "D06",
            "D08",
            "D09",
            "D10",
            "D12",
            "D13",
            "D20",
        ]
        return any(
            mesh_tree_number[0] in haystack
            for mesh_tree_number in self._mesh_tree_numbers
        )

    def compound_id(self) -> Optional[int]:
        """Return the PubChem Compound ID."""
        return self._compound_id

    def set_compound_id(self, compound_id: int) -> None:
        """Set the PubChem Compound ID."""
        self._compound_id = compound_id

    def substance_id(self) -> int:
        """Return the PubChem Substance ID."""
        return self._substance_id

    def set_substance_id(self, substance_id: int) -> None:
        """Set the PubChem Substance ID."""
        self._substance_id = substance_id

    def smiles(self) -> Optional[str]:
        """Return the SMILES string."""
        return self._smiles

    def set_smiles(self, smiles: str) -> None:
        """Set the SMILES string."""
        self._smiles = smiles

    def inchikey(self) -> Optional[str]:
        """Return the InChIKey."""
        return self._inchikey

    def set_inchikey(self, inchikey: str) -> None:
        """Set the InChIKey."""
        self._inchikey = inchikey

    @property
    def unique_identifier(self) -> str:
        """Return the unique identifier."""
        return self._unique_identifier

    @property
    def name(self) -> str:
        """Return the name of the descriptor."""
        return self._name


class MESHDescriptorsReader(MESHReader):
    """Class to read the MESH descriptors."""

    def __init__(self, settings: DatasetSettings):
        """Initialize the MESHDescriptorsReader class."""
        super().__init__(
            path=os.path.join(
                settings.downloads_directory,
                settings.descriptors_directory,
            ),
            verbose=settings.verbose,
        )
        self._allowed_mesh_tree_numbers: List[str] = settings.allowed_mesh_tree_numbers
        self._allowed_root_letters: List[str] = settings.allowed_root_letters

    def __iter__(self) -> Iterator[MESHDescriptor]:
        """Return the iterator."""
        for record in super().__iter__():
            assert record.record_type == "D"
            name = normalize_string(record["MH"][0])
            mesh_tree_numbers = [
                tree_number.split(".")
                for tree_number in record.get("MN", [])
                if tree_number[0] in self._allowed_root_letters
                and tree_number.split(".")[0] in self._allowed_mesh_tree_numbers
            ]
            descriptor = MESHDescriptor(
                name=name,
                unique_identifier=record.unique_identifier,
                mesh_tree_numbers=mesh_tree_numbers,
            )

            if not descriptor.has_mesh_tree_numbers():
                continue

            yield descriptor
