# IMAS Standard Names Catalog

YAML source files and pre-built SQLite database for IMAS Standard Names.

## Installation

### Python

```bash
pip install imas-standard-names-catalog
```

```python
from imas_standard_names_catalog import get_catalog_db
db_path = get_catalog_db()  # Path to bundled catalog.db
```

### Other Languages

Download from [releases](https://github.com/iterorganization/imas-standard-names-catalog/releases):

| Artifact | Description |
|----------|-------------|
| `catalog.db` | SQLite database |
| `standard_names.zip` | YAML sources + catalog.db |

### Development

```bash
git clone https://github.com/iterorganization/imas-standard-names-catalog.git
cd imas-standard-names-catalog
export STANDARD_NAMES_CATALOG_ROOT=$(pwd)/standard_names
```

**Build catalog locally:**
```bash
uv run standard-names build standard_names/
# Creates standard_names/.catalog/catalog.db
```

**Preview documentation site:**
```bash
uv run standard-names catalog-site serve standard_names/
# Serves at http://localhost:8000
```

**CI/CD Workflows:**

| Workflow | Trigger | Action |
|----------|---------|--------|
| `validate.yml` | PR, push to main | Validates YAML syntax |
| `catalog.yml` | Push to main/tags | Deploys versioned docs site |
| `release.yml` | Tag `v*` | Builds `catalog.db`, `standard_names.zip`, Python wheel |

## Structure

```
standard_names/     # YAML files by domain
src/                # Python package (catalog.db in wheel)
```

## Editing

Use MCP tools from [imas-standard-names](https://github.com/iterorganization/imas-standard-names). Never edit YAML directly.

## License

CC BY-ND 4.0
