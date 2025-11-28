# IMAS Standard Names Catalog

YAML source files for the IMAS Standard Names catalog.

## Installation

### For Users (Read-Only Access)

Download pre-built catalog from releases:

```bash
# Download catalog.db from latest release
wget https://github.com/iterorg/imas-standard-names-catalog/releases/latest/download/catalog.db

# Use with imas-standard-names
export STANDARD_NAMES_CATALOG_DB=/path/to/catalog.db
```

### For Developers (Read-Write Access)

Clone this repository and link to it:

```bash
# Clone catalog
git clone https://github.com/iterorg/imas-standard-names-catalog.git

# Link to catalog directory for development
export STANDARD_NAMES_CATALOG_ROOT=/path/to/imas-standard-names-catalog/standard_names
```

This environment variable must be set before using MCP tools from `imas-standard-names` to edit catalog entries.

## Repository Structure

- `standard_names/` - YAML catalog files organized by physics/diagnostic domain
- `.github/workflows/` - CI/CD automation for validation and releases
- Documentation files

## Editing Standard Names

Never edit YAML files directly. Use MCP tools from [`imas-standard-names`](https://github.com/iterorg/imas-standard-names):

```bash
# Set catalog location
export STANDARD_NAMES_CATALOG_ROOT=/path/to/imas-standard-names-catalog/standard_names

# Use MCP tools (see imas-standard-names AGENTS.md)
# mcp_sn_create_standard_names()
# mcp_sn_edit_standard_names()
# mcp_sn_write_standard_names()

# Commit changes
git add standard_names/
git commit -m "Add/modify standard names via MCP tools"
git push
```

## CI/CD

GitHub Actions validate YAML files on PRs and build `catalog.db` on releases using tools from `imas-standard-names`.

## License

CC BY-ND 4.0
