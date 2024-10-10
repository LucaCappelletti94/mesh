"""Data class defining a download objective."""

from dataclasses import dataclass


@dataclass
class DownloadObjective:
    """Data class defining a download objective."""

    path: str
    url: str
