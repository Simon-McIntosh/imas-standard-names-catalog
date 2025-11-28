# AGENTS.md - AI Agent Instructions

## Overview

This is a **data-only repository**. No Python code, no build tools, no application logic.

**Contents:**
- `standard_names/` - YAML catalog files organized by domain
- `.github/workflows/` - CI automation (uses `imas-standard-names` tools)
- Documentation and metadata only

## Critical Rules

### Never Edit YAML Files Directly

All catalog operations use MCP tools from [`imas-standard-names`](https://github.com/iterorg/imas-standard-names). See that repository's AGENTS.md for complete instructions.
### Link to This Catalog for Development

When developing or editing standard names, you must link to this catalog directory:

```bash
export STANDARD_NAMES_CATALOG_ROOT=/path/to/imas-standard-names-catalog/standard_names
```

This allows the MCP tools to read and write catalog entries. Without this environment variable set, the tools will use a read-only database instead.
### What You Can Do

- Update documentation (README, guides)
- Modify CI/CD workflows in `.github/workflows/`
- Update `.gitignore` for build artifacts
- Reorganize YAML file structure (move files between directories)

### What You Cannot Do

- Edit YAML files directly (use `imas-standard-names` MCP tools)
- Create Python modules or packages
- Implement validation/build logic
- Add Python dependencies to `pyproject.toml`
- Create test suites

## Version Control
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

## Workflow

**Working directory**: Commands assume you're in the project root (`/home/ITER/mcintos/Code/imas-standard-names`). Do NOT prefix with `cd /path/to/project &&`.

```bash
# 1. Set catalog location
export STANDARD_NAMES_CATALOG_ROOT=/path/to/imas-standard-names-catalog/standard_names

# 2. Use MCP tools from imas-standard-names to edit catalog
# (See imas-standard-names AGENTS.md)

# 3. Commit changes made by MCP tools
git add standard_names/
git commit -m "Add/modify standard names via MCP tools"
git push
```

## CI/CD

GitHub Actions validate YAML files on PRs and build `catalog.db` on releases using tools from the external `imas-standard-names` package.

## Integration

This catalog is consumed by [`imas-standard-names`](https://github.com/iterorg/imas-standard-names):

- **Development**: `export STANDARD_NAMES_CATALOG_ROOT=/path/to/standard_names`
---

**Remember**: This is a resource repository. All editing tools live in `imas-standard-names`.
