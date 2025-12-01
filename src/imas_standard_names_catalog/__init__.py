"""IMAS Standard Names Catalog.

Provides access to the bundled catalog.db for the IMAS Standard Names.
"""

from importlib.resources import files

__all__ = ["get_catalog_db"]


def get_catalog_db():
    """Return path to catalog.db (STANDARD_NAMES_CATALOG_DB).

    This is the pre-built SQLite database containing all standard names.
    Use this for read-only access without parsing YAML files.
    """
    return files("imas_standard_names_catalog") / "catalog.db"
