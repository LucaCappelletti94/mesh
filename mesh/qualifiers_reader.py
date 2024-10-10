"""Submodule providing a reader able to read the MESH qualifierss."""

import os
from typing import Iterator, List
from mesh.reader import MESHReader
from mesh.settings import DatasetSettings
from mesh.utils import normalize_string


class MESHQualifier:
    """Class representing a MESH qualifiers."""

    def __init__(self, name: str, unique_identifier: str):
        """Initialize the MESHQualifiers class."""
        self._name: str = name
        self._unique_identifier: str = unique_identifier

    def __repr__(self) -> str:
        """Return the representation of the MESH qualifiers."""
        return f"MESHQualifiers(name='{self._name}', id='{self._unique_identifier}')"

    @property
    def unique_identifier(self) -> str:
        """Return the unique identifier."""
        return self._unique_identifier

    @property
    def name(self) -> str:
        """Return the name of the qualifiers."""
        return self._name


class MESHQualifiersReader(MESHReader):
    """Class to read the MESH qualifierss."""

    def __init__(self, settings: DatasetSettings):
        """Initialize the MESHQualifierssReader class."""
        super().__init__(
            path=os.path.join(
                settings.downloads_directory,
                settings.qualifiers_directory,
            ),
            verbose=settings.verbose,
        )
        self._allowed_mesh_tree_numbers: List[str] = settings.allowed_mesh_tree_numbers
        self._allowed_root_letters: List[str] = settings.allowed_root_letters

    def __iter__(self) -> Iterator[MESHQualifier]:
        """Return the iterator."""
        for record in super().__iter__():
            assert (
                record.record_type == "Q"
            ), f"Invalid record type: {record.record_type}"
            name = normalize_string(record["SH"][0])
            qualifiers = MESHQualifier(
                name=name, unique_identifier=record.unique_identifier
            )

            yield qualifiers
