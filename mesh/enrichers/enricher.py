"""Submodule defining the Enricher interface."""

from abc import ABC, abstractmethod
from typing import Any


class Enricher(ABC):
    """Interface for enrichers."""

    @abstractmethod
    def name(self) -> str:
        """Return the name of the enricher."""

    @abstractmethod
    def enrich(self, entry: Any):
        """Enrich the data."""
