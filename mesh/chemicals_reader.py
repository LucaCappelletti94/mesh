"""Submodule providing a reader able to read the MESH descriptors."""

import os
from typing import Iterator, List
from mesh.reader import MESHReader
from mesh.settings import DatasetSettings
from mesh.utils import normalize_string


class MESHChemical:
    """Class representing a MESH descriptor."""

    def __init__(
        self,
        name: str,
        unique_identifier: str,
        pharmacological_actions: List[str],
        descriptors: List[str],
        qualifiers: List[str],
    ):
        """Initialize the MESHChemical class."""
        self._name: str = name
        self._unique_identifier: str = unique_identifier
        self._pharmacological_actions: List[str] = pharmacological_actions
        self._descriptors: List[str] = descriptors
        self._qualifiers: List[str] = qualifiers

    def __repr__(self) -> str:
        """Return the representation of the MESH descriptor."""
        return f"MESHChemical(name='{self._name}', pharmacological_actions={self._pharmacological_actions}, descriptors={self._descriptors}, qualifiers={self._qualifiers})"

    @property
    def unique_identifier(self) -> str:
        """Return the unique identifier."""
        return self._unique_identifier

    @property
    def name(self) -> str:
        """Return the name of the descriptor."""
        return self._name


class MESHChemicalsReader(MESHReader):
    """Class to read the MESH descriptors."""

    def __init__(self, settings: DatasetSettings):
        """Initialize the MESHChemicalsReader class."""
        super().__init__(
            path=os.path.join(
                settings.download_directory,
                settings.chemicals_directory,
            ),
            verbose=settings.verbose,
        )

    def __iter__(self) -> Iterator[MESHChemical]:
        """Return the iterator."""
        for record in super().__iter__():
            assert record.record_type == "C", f"Invalid record type: {record.record_type}"
            name = normalize_string(record["NM"][0])
            pharmacological_actions = [
                action.split("-")[0]
                for action in record.get("PA", [])
            ]
            descriptors: List[str] = []
            qualifiers: List[str] = []
            for headings in record.get("HM", []):
                for heading in headings.split("/"):
                    heading = heading.split("-")[0].strip(" *")
                    if heading.startswith("Q"):
                        qualifiers.append(heading)
                    elif heading.startswith("D"):
                        descriptors.append(heading)
                    else:
                        raise ValueError(f"Invalid heading: {heading}")

            chemical = MESHChemical(
                name=name,
                unique_identifier=record.unique_identifier,
                pharmacological_actions=pharmacological_actions,
                descriptors=descriptors,
                qualifiers=qualifiers,
            )

            yield chemical
