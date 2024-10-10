"""Submodule providing a reader able to iterate over the MESH formats."""

from typing import List, Dict, Optional, Iterator
from tqdm.auto import tqdm


class MESHRecord:
    """Class representing a MESH record."""

    def __init__(self):
        """Initialize the MESH record."""
        self._record: Dict[str, List[str]] = {}
        self._record_type: Optional[str] = None
        self._unique_identifier: Optional[str] = None

    def is_complete(self) -> bool:
        """Return whether the record is complete."""
        return (
            self._record_type is not None
            and self._unique_identifier is not None
            and len(self._record) > 0
        )

    @property
    def record_type(self) -> str:
        """Return the record type."""
        assert self._record_type is not None
        return self._record_type

    @property
    def unique_identifier(self) -> str:
        """Return the unique identifier."""
        assert self._unique_identifier is not None
        return self._unique_identifier

    def set_record_type(self, record_type: str):
        """Set the record type."""
        assert self._record_type is None
        assert record_type in ["C", "D", "Q"], f"Invalid record type: {record_type}"
        self._record_type = record_type

    def set_unique_identifier(self, unique_identifier: str):
        """Set the unique identifier."""
        assert self._unique_identifier is None
        assert self._record_type is not None
        assert unique_identifier.startswith(
            self._record_type
        ), f"Invalid unique identifier: {unique_identifier}"
        # All terms of the unique identifier after the first character are digits
        assert unique_identifier[
            1:
        ].isdigit(), f"Invalid unique identifier: {unique_identifier}"

        self._unique_identifier = unique_identifier

    def __contains__(self, key: str) -> bool:
        """Return whether the key is in the record."""
        return key in self._record

    def __getitem__(self, key: str) -> List[str]:
        """Return the value of the key."""
        assert key in self._record, f"Key not found: {key}"
        return self._record[key]

    def get(self, key: str, default: Optional[List[str]] = None) -> Optional[List[str]]:
        """Return the value of the key or a default value."""
        return self._record.get(key, default)

    def add_key_value(self, key: str, value: str):
        """Add a key-value pair."""
        assert len(key) > 0
        assert len(value) > 0
        if key not in self._record:
            self._record[key] = []
        self._record[key].append(value)

    def __repr__(self) -> str:
        """Return the string representation of the record."""
        return f"MESHRecord({self._record_type}, {self._unique_identifier}, {self._record})"


class MESHReader:
    """Class representing a MESH reader."""

    def __init__(self, path: str, verbose: bool = False):
        """Initialize the MESH reader."""
        self._path: str = path
        self._verbose: bool = verbose

    def __iter__(self) -> Iterator[MESHRecord]:
        """Iterate over the MESH file."""
        loading_bar = tqdm(
            desc="Loading MESH records",
            unit="record",
            dynamic_ncols=True,
            leave=False,
            disable=not self._verbose,
        )
        with open(self._path, "r", encoding="utf8") as file:
            record: Optional[MESHRecord] = None
            for line in file:
                line = line.strip()

                if len(line) == 0:
                    continue

                if line == "*NEWRECORD":
                    if record is not None:
                        loading_bar.update(1)
                        assert record.is_complete(), "Incomplete record."
                        yield record
                    record = MESHRecord()
                    continue

                assert " = " in line

                key, value = line.split(" = ", 1)

                assert len(key) > 0
                assert len(value) > 0

                if key == "RECTYPE":
                    record.set_record_type(value)
                    continue

                if key == "UI":
                    record.set_unique_identifier(value)
                    continue

                record.add_key_value(key, value)

            if record.record_type is not None:
                yield record
