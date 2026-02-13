"""pyvariantdb - A python package to download, process and access dbSNP data."""

import sys
from pathlib import Path

__all__ = ["__version__"]


def _get_version() -> str:
    """Parse version from pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

    if pyproject_path.exists():
        # Try tomllib (Python 3.11+) or tomli (fallback)
        try:
            if sys.version_info >= (3, 11):
                import tomllib
            else:
                import tomli as tomllib  # type: ignore

            with open(pyproject_path, "rb") as f:
                pyproject_data = tomllib.load(f)
                return pyproject_data.get("project", {}).get("version", "unknown")
        except ImportError:
            # Fallback: parse manually if no toml library available
            with open(pyproject_path, "r") as f:
                for line in f:
                    if line.strip().startswith("version"):
                        # Extract version from 'version = "1.0"'
                        return line.split("=")[1].strip().strip('"').strip("'")

    return "unknown"


__version__ = _get_version()
