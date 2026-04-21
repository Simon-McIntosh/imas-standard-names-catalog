# IMAS Standard Names Catalog

YAML source files and pre-built SQLite database for IMAS Standard Names.

> **Schema v2 clean break.** This catalog is regenerated from the
> [imas-codex](https://github.com/Simon-McIntosh/imas-codex) knowledge graph.
> Prior entries from schema v1 are deprecated. Do not manually merge old YAML
> files — use `sn export` to regenerate from the graph.

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
# Or from imas-codex: imas-codex sn preview --staging ./staging
```

**CI/CD Workflows:**

| Workflow | Trigger | Action |
|----------|---------|--------|
| `validate.yml` | PR, push to main | Validates YAML syntax |
| `catalog.yml` | Push to main/tags | Deploys versioned docs site |
| `release.yml` | Tag `v*` | Builds `catalog.db`, `standard_names.zip`, Python wheel |

## Structure

```
standard_names/
  <physics_domain>/          # Directory per PhysicsDomain enum value
    <standard_name>.yml      # One file per standard name
src/                         # Python package (catalog.db in wheel)
```

Each YAML file contains a single `StandardNameEntry`: name, description,
documentation, unit, kind, tags, links, grammar fields, COCOS metadata,
and provenance (origin, status, scores).

## Editing

Edit YAML files via pull request. The PR workflow:

1. Edit `standard_names/<domain>/<name>.yml` — change description, documentation, tags, kind, links, or status
2. Open a PR against `main`
3. CI validates YAML syntax
4. Reviewer approves and merges
5. From imas-codex: `imas-codex sn import --isnc <path-to-this-repo>` reads the merged changes, detects edits to protected fields, and flips `origin=catalog_edit` on modified names. Subsequent pipeline runs preserve these edits.

**Quality gate context:** Only names passing `reviewer_score >= 0.65` and
a valid `description_score` are exported from imas-codex to this catalog.
Names below threshold are regenerated in the pipeline before export.

## License

CC BY-ND 4.0
