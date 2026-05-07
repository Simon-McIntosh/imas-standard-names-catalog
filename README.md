# IMAS Standard Names Catalog

[![Catalog Site](https://github.com/Simon-McIntosh/imas-standard-names-catalog/actions/workflows/catalog.yml/badge.svg)](https://github.com/Simon-McIntosh/imas-standard-names-catalog/actions/workflows/catalog.yml)
[![Validate](https://github.com/Simon-McIntosh/imas-standard-names-catalog/actions/workflows/validate.yml/badge.svg)](https://github.com/Simon-McIntosh/imas-standard-names-catalog/actions/workflows/validate.yml)
[![Docs](https://img.shields.io/badge/docs-catalog%20site-blue)](https://simon-mcintosh.github.io/imas-standard-names-catalog/)

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
catalog.yml                  # Export metadata (provenance, quality gates)
src/                         # Python package (catalog.db bundled in wheel)
```

Each domain YAML file contains a list of `StandardNameEntry` objects with: name,
description, documentation, unit, kind, tags, links, grammar fields, COCOS
metadata, and provenance (origin, status, scores).

## CI/CD Workflows

| Workflow | Trigger | Action |
|----------|---------|--------|
| `validate.yml` | PR, push to main | Validates YAML syntax and catalog consistency |
| `catalog.yml` | Push to main/tags | Builds versioned docs site via mike → gh-pages |
| `release.yml` | Tag `v*` | Builds `catalog.db`, `standard_names.zip`, Python wheel |

## Editing

Edit YAML files via pull request. The PR workflow:

1. Edit `standard_names/<domain>.yml` — change description, documentation,
   tags, kind, links, or status
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
