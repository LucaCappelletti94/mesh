"""Submodule providing a reader able to read the MESH descriptors."""

import os
from typing import Iterator, List, Optional, Dict, Any
from mesh.reader import MESHReader
from mesh.settings import DatasetSettings
from mesh.utils import normalize_string, MaybeChemical


class MESHChemical(MaybeChemical):
    """Class representing a MESH descriptor."""

    def __init__(
        self,
        name: str,
        unique_identifier: str,
        pharmacological_actions: List[str],
        descriptors: List[str],
    ):
        """Initialize the MESHChemical class."""
        self._name: str = name
        self._unique_identifier: str = unique_identifier
        self._pharmacological_actions: List[str] = pharmacological_actions
        self._descriptors: List[str] = descriptors
        self._compound_id: Optional[int] = None
        self._substance_id: Optional[int] = None
        self._smiles: Optional[str] = None
        self._inchikey: Optional[str] = None
        self._inchi: Optional[str] = None

    def chemical_name(self) -> str:
        """Return the chemical name."""
        return self._name

    def maybe_chemical(self) -> bool:
        """Return whether the descriptor is a chemical."""
        return True

    def compound_id(self) -> int:
        """Return the PubChem Compound ID."""
        return self._compound_id

    def set_compound_id(self, compound_id: int) -> None:
        """Set the PubChem Compound ID."""
        assert isinstance(compound_id, int), f"Invalid compound ID: {compound_id}"
        self._compound_id = compound_id

    def substance_id(self) -> int:
        """Return the PubChem Substance ID."""
        return self._substance_id

    def set_substance_id(self, substance_id: int) -> None:
        """Set the PubChem Substance ID."""
        assert isinstance(substance_id, int), f"Invalid substance ID: {substance_id}"
        self._substance_id = substance_id

    def smiles(self) -> str:
        """Return the SMILES string."""
        return self._smiles

    def set_smiles(self, smiles: str) -> None:
        """Set the SMILES string."""
        self._smiles = smiles

    def inchikey(self) -> str:
        """Return the InChIKey."""
        return self._inchikey

    def inchi(self) -> str:
        """Return the InChI."""
        return self._inchi

    def set_inchi_and_inchikey(self, inchi: str, inchikey: str) -> None:
        """Set the InChIKey."""
        self._inchi = inchi
        self._inchikey = inchikey

    @property
    def descriptors(self) -> List[str]:
        """Return the descriptors."""
        return self._descriptors

    @property
    def pharmacological_actions(self) -> List[str]:
        """Return the pharmacological actions."""
        return self._pharmacological_actions

    def __repr__(self) -> str:
        """Return the representation of the MESH descriptor."""
        return f"MESHChemical(name='{self._name}', pharmacological_actions={self._pharmacological_actions}, descriptors={self._descriptors}, compound_id={self._compound_id}, substance_id={self._substance_id}, smiles={self._smiles}, inchikey={self._inchikey})"

    @property
    def unique_identifier(self) -> str:
        """Return the unique identifier."""
        return self._unique_identifier

    @property
    def name(self) -> str:
        """Return the name of the descriptor."""
        return self._name

    def into_dict(self) -> Dict[str, Any]:
        """Return the MESH descriptor as a dictionary."""
        return {
            "unique_identifier": self.unique_identifier,
            "name": self.chemical_name(),
            "compound_id": self.compound_id(),
            "substance_id": self.substance_id(),
            "smiles": self.smiles(),
            "inchi": self._inchi,
            "inchikey": self.inchikey(),
        }


class MESHChemicalsReader(MESHReader):
    """Class to read the MESH descriptors."""

    def __init__(self, settings: DatasetSettings):
        """Initialize the MESHChemicalsReader class."""
        super().__init__(
            path=os.path.join(
                settings.downloads_directory,
                settings.chemicals_directory,
            ),
            verbose=settings.verbose,
        )

    def __iter__(self) -> Iterator[MESHChemical]:
        """Return the iterator."""
        for record in super().__iter__():
            assert (
                record.record_type == "C"
            ), f"Invalid record type: {record.record_type}"
            name = normalize_string(record["NM"][0])
            pharmacological_actions = [
                action.split("-")[0] for action in record.get("PA", [])
            ]
            descriptors: List[str] = []
            for headings in record.get("HM", []):
                for heading in headings.split("/"):
                    heading = heading.split("-")[0].strip(" *")
                    if heading.startswith("Q"):
                        continue
                    elif heading.startswith("D"):
                        descriptors.append(heading)
                    else:
                        raise ValueError(f"Invalid heading: {heading}")

            chemical = MESHChemical(
                name=name,
                unique_identifier=record.unique_identifier,
                pharmacological_actions=pharmacological_actions,
                descriptors=descriptors,
            )

            yield chemical
