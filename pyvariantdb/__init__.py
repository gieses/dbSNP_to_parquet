"""pyvariantdb - A python package to download, process and access dbSNP data."""

import importlib.metadata as importlib_metadata

__all__ = ["__version__"]

__version__ = importlib_metadata.version(__name__)
