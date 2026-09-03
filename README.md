# IMAS Standard Names Catalog

[![Catalog Site](https://github.com/Simon-McIntosh/imas-standard-names-catalog/actions/workflows/catalog.yml/badge.svg)](https://github.com/Simon-McIntosh/imas-standard-names-catalog/actions/workflows/catalog.yml)
[![Validate](https://github.com/Simon-McIntosh/imas-standard-names-catalog/actions/workflows/validate.yml/badge.svg)](https://github.com/Simon-McIntosh/imas-standard-names-catalog/actions/workflows/validate.yml)
[![Docs](https://img.shields.io/badge/docs-catalog%20site-blue)](https://simon-mcintosh.github.io/imas-standard-names-catalog/)

YAML source files and pre-built SQLite database for IMAS Standard Names.

Generated from the [imas-codex](https://github.com/Simon-McIntosh/imas-codex) knowledge graph via `imas-codex sn export`.

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
uv sync
```

**Build catalog locally:**
```bash
uv run standard-names build standard_names/
# Creates standard_names/.catalog/catalog.db
```

**Preview documentation site:**
```bash
uv run standard-names site-serve standard_names/
# Serves at http://localhost:8000
```

## Structure

```
standard_names/
  <physics_domain>.yml       # One file per physics domain (list of entries)
catalog.yml                  # Export metadata and the per-name machine-owned block
src/                         # Python package (catalog.db bundled in wheel)
```

Each domain YAML file contains a list of entries, and each entry carries only
the four review fields: the standard name, its description, its documentation,
and its unit. Everything the pipeline owns — the entry kind, its lifecycle
status, its physics domain, its Data Dictionary source bindings, its
cross-reference links, and its generated identity roles — is carried per name in
the `catalog.yml` sidecar, alongside the export provenance and the quality
gates. The catalog site reads both files and renders one page per name.

## CI/CD Workflows

| Workflow | Trigger | Action |
|----------|---------|--------|
| `validate.yml` | PR, push to main | Validates YAML syntax and catalog consistency |
| `catalog.yml` | Push to main/tags | Builds versioned docs site via mike → gh-pages |
| `release.yml` | Tag `v*` | Builds `catalog.db`, `standard_names.zip`, Python wheel |

## Editing

Edit YAML files via pull request. The PR workflow:

1. Edit `standard_names/<domain>.yml` — change the standard name, its
   description, or its documentation. The sidecar is machine-owned; a hand edit
   to it is rejected by CI
2. Open a PR against `main`
3. CI validates YAML syntax
4. Reviewer approves and merges
5. From imas-codex: `imas-codex sn import --isnc <path>` reads the merged
   changes, detects edits to protected fields, and flips `origin=catalog_edit`
   on modified names. Subsequent pipeline runs preserve these edits.

**Quality gates:** Only names passing `reviewer_score >= 0.65` and a valid
`description_score` are exported from imas-codex to this catalog. Names below
threshold are regenerated in the pipeline before export.

## License

CC BY-ND 4.0
