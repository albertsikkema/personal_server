# PRP: Migrate from pip to uv Package Manager

## Feature: Complete migration from pip to uv for improved dependency management and development workflow

### Overview
Migrate the FastAPI application from pip-based dependency management to uv, a modern, high-performance Python package manager. This migration will modernize the development workflow, improve dependency resolution speed, and provide better reproducibility through unified project management.

### Context & Documentation

#### UV Documentation
- **Official Documentation**: https://docs.astral.sh/uv/
- **Migration Guide**: https://docs.astral.sh/uv/guides/migration/pip-to-project/
- **Project Management**: https://docs.astral.sh/uv/guides/projects/
- **Package Management**: https://docs.astral.sh/uv/pip/packages/
- **GitHub Repository**: https://github.com/astral-sh/uv

#### Key UV Migration Patterns

**Basic Migration from requirements.txt:**
```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create minimal project structure
uv init --bare

# Import existing requirements
uv add -r requirements.txt

# Import development requirements
uv add --dev -r requirements-dev.txt

# Clean up old files
rm requirements.txt
```

**Project Environment Management:**
```bash
# Create and sync environment
uv sync

# Run commands in project environment
uv run python main.py
uv run pytest
uv run ruff check .

# Add/remove dependencies
uv add requests
uv remove requests
uv add --dev pytest
```

**pyproject.toml Configuration:**
```toml
[project]
name = "fastapi-app"
version = "1.0.0"
description = "A FastAPI application with API key authentication"
authors = [{name = "FastAPI App", email = "app@example.com"}]
requires-python = ">=3.9"
dependencies = [
    "fastapi[standard]",
    "pydantic>=2.0",
    "pydantic-settings",
    "uvicorn",
    "slowapi",
    "httpx",
    "fastmcp",
]

[dependency-groups]
dev = [
    "pytest",
    "pytest-asyncio",
    "pytest-cov",
    "ruff",
    "coverage",
]

[tool.uv]
dev-dependencies = [
    "pytest-xdist",
]
```

### Current State Analysis

#### Current pip Usage Patterns (from codebase analysis)

**Makefile Commands:**
```makefile
# Current pip-based commands
setup: 
	python -m venv venv
	source venv/bin/activate && pip install --upgrade pip
	source venv/bin/activate && pip install -r requirements.txt

install:
	source venv/bin/activate && pip install --upgrade pip
	source venv/bin/activate && pip install -r requirements.txt

freeze:
	source venv/bin/activate && pip freeze > requirements.txt

update:
	source venv/bin/activate && pip install --upgrade pip
	source venv/bin/activate && pip install --upgrade -r requirements.txt
```

**Current Dependencies (from requirements.txt):**
- 46 pinned dependencies with exact versions
- Mix of direct and transitive dependencies
- No separation between dev and production dependencies

**Current Project Structure Issues:**
- `requirements.txt` with pinned versions (should be replaced with pyproject.toml)
- `pyproject.toml` with minimal dependencies (needs to be expanded)
- `uv.lock` exists but not being used in development workflow
- `venv/` directory (should be replaced with `.venv`)
- `fastapi_app.egg-info/` directory (pip-specific, should be removed)

### Implementation Plan

#### Phase 1: Environment Setup and Dependency Migration

1. **Update pyproject.toml with all dependencies**
   - Extract all dependencies from requirements.txt
   - Organize into main dependencies and dev dependencies
   - Set appropriate version constraints (avoid pinning unless necessary)
   - Add Python version requirement

2. **Import existing requirements**
   - Use `uv add -r requirements.txt` to import all current dependencies
   - Verify that all dependencies are captured correctly
   - Handle any conflicts or version issues

3. **Update development dependencies**
   - Identify development-only dependencies
   - Move test, linting, and build tools to dev dependencies
   - Use `uv add --dev` for development dependencies

#### Phase 2: Build System and Tool Configuration

1. **Update Makefile for uv commands**
   - Replace all pip commands with uv equivalents
   - Update virtual environment creation
   - Modify run commands to use `uv run`
   - Update dependency management commands

2. **Update .gitignore**
   - Remove pip-specific entries (pip-wheel-metadata)
   - Add uv-specific entries if needed
   - Keep `.venv/` (uv's standard virtual environment location)

3. **Clean up obsolete files**
   - Remove requirements.txt after successful migration
   - Remove fastapi_app.egg-info/ directory
   - Remove old venv/ directory in favor of .venv/

#### Phase 3: Documentation and Workflow Updates

1. **Update README.md**
   - Replace pip installation instructions with uv commands
   - Update development setup instructions
   - Update dependency management examples

2. **Update Claude.md**
   - Ensure all uv documentation is accurate
   - Update development workflow patterns
   - Add migration completion notes

3. **Update development commands**
   - Test all Makefile commands
   - Verify that all development workflows work
   - Update CI/CD if applicable

### Validation Gates

#### Syntax and Configuration Validation
```bash
# Validate pyproject.toml syntax
uv tree

# Check for dependency conflicts
uv sync --frozen

# Validate that all dependencies are resolvable
uv lock --check
```

#### Development Environment Validation
```bash
# Test that development environment works
uv run python -c "import fastapi; print('FastAPI imported successfully')"
uv run python -c "import pydantic; print('Pydantic imported successfully')"
uv run python -c "import uvicorn; print('Uvicorn imported successfully')"

# Test that all services start correctly
uv run fastapi dev main.py &
sleep 5
curl -f http://localhost:8000/health
kill %1
```

#### Testing and Code Quality Validation
```bash
# Run complete test suite
uv run pytest

# Run with coverage
uv run pytest --cov=. --cov-report=term-missing

# Run linting and formatting
uv run ruff check .
uv run ruff format --check .
```

#### Application Functionality Validation
```bash
# Test main application functionality
uv run python -m pytest tests/test_integration.py -v

# Test specific features
uv run python -m pytest tests/test_geocoding_service.py -v
uv run python -m pytest tests/test_crawling_service.py -v

# Test MCP integration
uv run python -c "from mcp_integration.server import get_mcp_server; print('MCP server imported successfully')"
```

### Success Criteria

1. **Complete pip removal**: No pip commands remain in any project files
2. **Functional parity**: All existing functionality works identically
3. **Performance improvement**: Dependency installation is faster with uv
4. **Reproducible builds**: uv.lock ensures consistent environments
5. **Clean project structure**: Modern Python packaging standards followed
6. **Documentation accuracy**: All docs reflect uv usage
7. **Developer experience**: Simplified workflow with unified tooling

### Risk Mitigation

#### Dependency Conflicts
- **Risk**: Some dependencies may have version conflicts when migrated
- **Mitigation**: Use `uv tree` to identify conflicts and resolve manually
- **Backup**: Keep requirements.txt until migration is fully validated

#### Development Workflow Disruption
- **Risk**: Developers may be unfamiliar with uv commands
- **Mitigation**: Provide comprehensive documentation and examples
- **Backup**: Maintain Makefile commands for common operations

#### Hidden Dependencies
- **Risk**: Some implicit dependencies may be missed
- **Mitigation**: Thorough testing of all application functionality
- **Backup**: Review requirements.txt manually for any missed dependencies

### Implementation Tasks (Ordered)

1. **Backup current state**
   - Create git branch for migration
   - Document current working state

2. **Update pyproject.toml**
   - Add all dependencies from requirements.txt
   - Organize into main and dev dependencies
   - Set appropriate version constraints

3. **Import dependencies with uv**
   - Run `uv add -r requirements.txt`
   - Verify uv.lock is updated correctly
   - Test that environment syncs properly

4. **Update Makefile**
   - Replace all pip commands with uv equivalents
   - Update virtual environment handling
   - Test all make commands

5. **Update documentation**
   - Modify README.md installation instructions
   - Update Claude.md with migration completion
   - Update any other documentation references

6. **Clean up obsolete files**
   - Remove requirements.txt
   - Remove fastapi_app.egg-info/
   - Update .gitignore

7. **Comprehensive testing**
   - Run all validation gates
   - Test complete development workflow
   - Verify application functionality

8. **Documentation finalization**
   - Update any remaining references
   - Add migration notes to project history

### Post-Migration Benefits

1. **Performance**: 10-100x faster dependency resolution and installation
2. **Reliability**: Unified lockfile ensures reproducible environments
3. **Simplicity**: Single tool replaces pip, pip-tools, virtualenv
4. **Modernity**: Follows current Python packaging standards
5. **Maintainability**: Cleaner project structure and dependency management

### Confidence Score: 9/10

This migration is highly likely to succeed in one-pass implementation because:
- UV provides excellent pip compatibility
- Comprehensive documentation and examples available
- Clear validation gates ensure nothing is missed
- Risk mitigation strategies address potential issues
- Current project structure is already partially prepared (uv.lock exists)
- Modern Python packaging practices are well-established

The only minor risk is potential dependency conflicts, but these can be resolved through careful testing and the provided validation gates.