# Catalog Repository CLI Interface

This document defines the CLI interface between `imas-standard-names` and the `imas-standard-names-catalog` repository. The catalog repository is designed as a zero-code repository containing only YAML standard name definitions.

## Overview

The `imas-standard-names` package provides CLI commands that the catalog repository uses in its CI workflows:

| Command | Purpose | Exit Codes |
|---------|---------|------------|
| `validate_catalog` | Validate YAML files | 0=pass, 1=fail, 2=integrity issues |
| `standard-names build` | Build catalog.db | 0=success, 1=error |
| `standard-names docs` | Build documentation site | 0=success, 1=error |

## Installation

The catalog repository specifies `imas-standard-names` as a dev dependency:

```toml
# In catalog repo pyproject.toml
[dependency-groups]
dev = [
    "imas-standard-names[quality] @ git+https://github.com/iterorganization/imas-standard-names.git",
]
```

Then in CI, `uv run` automatically syncs and runs commands:

```yaml
- run: uv run validate_catalog standard_names/
```

## CLI Commands

### Validate Catalog

Validates YAML structure, grammar, and quality checks.

```bash
validate_catalog <catalog_path> [OPTIONS]
```

**Arguments:**
- `catalog_path` — Path to directory containing YAML standard name files

**Options:**
- `--mode [auto|file|memory]` — Source mode (default: auto)
- `--verify` — Verify integrity table (file mode only)
- `--full` — When verifying, recompute hashes even if metadata matches
- `--quality-check/--no-quality-check` — Enable or disable quality checks (default: enabled). Requires `quality` extra.
- `--strict` — Fail validation on quality warnings (not just errors)
- `--summary [text|json]` — Output machine-readable summary

**Examples:**

```bash
# Basic validation with quality checks
validate_catalog standard_names/

# Skip quality checks (faster, for quick validation)
validate_catalog standard_names/ --no-quality-check

# CI-friendly summary output
validate_catalog standard_names/ --summary text
# Output: ✓ Validated 305 entries (0 errors, 134 warnings)

# Strict mode: fail on any quality warnings
validate_catalog standard_names/ --strict --summary text

# JSON output for programmatic parsing
validate_catalog standard_names/ --summary json
# Output: {"passed": true, "entries": 305, "errors": 0, "warnings": 134, "info": 0}
```

**Exit Codes:**
- `0` — Validation passed
- `1` — Validation failed (errors found, or warnings in strict mode)
- `2` — Integrity issues detected

---

### Build Catalog Database

Builds SQLite catalog from YAML files.

```bash
standard-names build <catalog_path> [OPTIONS]
```

**Arguments:**
- `catalog_path` — Path to directory containing YAML standard name files

**Options:**
- `--db <path>` — Output database path (default: `<catalog_path>/.catalog/catalog.db`)
- `--verify` — Output verification summary with file size and entry count
- `--overwrite/--no-overwrite` — Overwrite existing DB (default: overwrite)

**Examples:**

```bash
# Basic build
standard-names build standard_names/

# Build with verification output (recommended for CI)
standard-names build standard_names/ --db catalog.db --verify
# Output: ✓ Built catalog.db: 45.2 KB, 305 entries
```

---

### Build Documentation

Generates and deploys versioned documentation using mkdocs + mike.

```bash
standard-names docs build <catalog_path> --version <version> [OPTIONS]
```

**Arguments:**
- `catalog_path` — Path to directory containing YAML standard name files

**Options:**
- `--version <version>` — Version string (required, e.g., "v0.1", "main", "pr-123")
- `--site-name <name>` — Site name (default: "Standard Names Catalog")
- `--site-url <url>` — Site URL
- `--push` — Push to gh-pages branch
- `--set-default` — Set this version as the default (latest)
- `--output <path>` — Output directory (default: temporary)

**Examples:**

```bash
# Build and push version
standard-names docs build standard_names/ --version v1.0.0 --push

# Build, push, and set as default
standard-names docs build standard_names/ --version v1.0.0 --push --set-default

# Build for PR preview (no push)
standard-names docs build standard_names/ --version pr-123 --output ./site
```

**Version Aliasing:**

```bash
standard-names docs alias --version v1.0.0 --alias latest --push
```

**Requirements:**
- Git repository with gh-pages branch configured
- `mike` and `mkdocs-material` are bundled with `imas-standard-names`

---

## CI Workflow Example

```yaml
name: Catalog CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v5
      
      - name: Validate catalog
        run: uv run validate_catalog standard_names/ --summary text
      
      - name: Build catalog database
        run: uv run standard-names build standard_names/ --db catalog.db

  docs:
    runs-on: ubuntu-latest
    needs: validate
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Install uv
        uses: astral-sh/setup-uv@v5
      
      - name: Configure git
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
      
      - name: Deploy docs
        run: |
          git fetch origin gh-pages --depth=1 || echo "No gh-pages branch yet"
          uv run standard-names docs build standard_names/ \
            --version ${{ github.ref_name }} --push --set-default
```

---

## Documentation Content

The `standard-names docs build` command generates:

1. **index.md** — From catalog's `README.md` if present, otherwise auto-generated overview
2. **catalog.md** — Complete browsable catalog organized by primary tag and base name

The generated site includes:
- Full-text search
- Version selector (via mike)
- Responsive material theme
- Anchor links for each standard name

---

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `STANDARD_NAMES_CATALOG_ROOT` | Default catalog path for MCP server and tools |

---

## Version Compatibility

This interface is provided by `imas-standard-names` version 0.X.Y and later. The catalog repository should pin to a compatible version range to ensure CI stability.
