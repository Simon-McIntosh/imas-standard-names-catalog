# AI Agent Instructions

## Overview

This is a data-only repository containing YAML source files for the IMAS Standard Names catalog. No Python code, no build tools, no application logic.

**Never edit YAML files directly.** Use MCP tools from the [`imas-standard-names`](https://github.com/iterorg/imas-standard-names) package. See that repository's AGENTS.md for complete instructions.

## Linking to This Catalog

```bash
# Development: Use local YAML files
export STANDARD_NAMES_CATALOG_ROOT=/path/to/imas-standard-names-catalog/standard_names

# Production: Use pre-built catalog.db
export STANDARD_NAMES_CATALOG_DB=/path/to/catalog.db
```

## Repository Contents

- `standard_names/` - YAML catalog files organized by physics domain
- `.github/workflows/` - CI/CD automation for validation and releases
- `README.md`, `catalog-development-guide.md` - Documentation
- `pyproject.toml` - Version metadata only

## Terminal Usage

**Working directory**: Commands assume you're in the project root (`/home/ITER/mcintos/Code/imas-standard-names`). Do NOT prefix with `cd /path/to/project &&`.

## What You Can Do

- Update documentation (README)
- Modify CI/CD workflows in `.github/workflows/`
- Update `.gitignore` for build artifacts

## What You Cannot Do

- Edit YAML files directly (use `imas-standard-names` MCP tools)
- Create Python modules or packages
- Implement validation/build logic
- Add Python dependencies to `pyproject.toml`
- Create test suites

## Modifying Standard Names

All catalog operations use MCP tools from [`imas-standard-names`](https://github.com/iterorg/imas-standard-names):

- `create_standard_names()` - Add new entries
- `edit_standard_names()` - Modify/rename/delete entries
- `list_standard_names(scope='pending')` - Review pending changes
- `write_standard_names()` - Write to disk (requires user permission)

See the `imas-standard-names` AGENTS.md for detailed workflows.

## CI/CD

GitHub Actions validate YAML files on PRs and build `catalog.db` on releases using tools from the external `imas-standard-names` package.

## Version Control

Semantic versioning: `vX.Y.Z`
- Major: Breaking changes to existing names
- Minor: New standard names added
- Patch: Documentation/metadata updates

Release tags trigger CI build and deployment.

### Version Control
- **Branch naming**: Use `main` as default branch
- **GitHub CLI**: `gh` is installed in `~/.local/bin` and available in PATH
- **Authentication**: SSH
- **Commit messages**: Use conventional commit format with detailed body

**Common gh commands**:
```bash
gh repo create <name> --public --description "..."  # Create repository
gh repo edit --default-branch main                  # Change default branch
gh pr create --title "..." --body "..."             # Create pull request
gh issue create --title "..." --body "..."          # Create issue
gh repo view --web                                  # Open repo in browser
```

**Git workflow**:
```bash
git status                      # Check current state
git add -A                      # Stage all changes
git commit -m "message"         # Commit with message (triggers pre-commit)
git push origin main            # Push to remote
git pull origin main            # Pull latest changes
```

## Common Tasks

**Add/modify standard names**: See `imas-standard-names` AGENTS.md for MCP tool workflows

**Trigger release**:
```bash
git tag -a v1.0.0 -m "Release description"
git push origin v1.0.0
```

## See also

- Standard name operations: `imas-standard-names` AGENTS.md
- Build/validation: `imas-standard-names` documentation
- CI/CD: `.github/workflows/` and GitHub Actions logs

