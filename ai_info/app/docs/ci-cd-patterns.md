# CI/CD Pipeline Implementation Patterns

This document contains comprehensive CI/CD pipeline patterns using GitHub Actions with modern best practices for Python projects using uv.

## GitHub Actions Workflow Structure

### Quality and Testing Workflow

```yaml
# .github/workflows/quality.yml
name: Quality & Testing

on:
  push:
    branches: [main, dev]
    paths:
      - '**.py'
      - 'pyproject.toml'
      - 'uv.lock'
      - 'Makefile'
      - '.github/workflows/**'
  pull_request:
    branches: [main, dev]
    paths:
      - '**.py'
      - 'pyproject.toml'
      - 'uv.lock'
      - 'Makefile'
      - '.github/workflows/**'
  workflow_dispatch:  # Manual trigger

env:
  UV_CACHE_DIR: /tmp/.uv-cache

jobs:
  changes:
    name: Detect Changes
    runs-on: ubuntu-latest
    outputs:
      python: ${{ steps.changes.outputs.python }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: changes
        with:
          filters: |
            python:
              - '**.py'
              - 'pyproject.toml'
              - 'uv.lock'
              - 'Makefile'
```

## uv Integration Pattern

### High-Performance Python Setup

```yaml
# High-performance Python setup with uv
- name: Install uv
  uses: astral-sh/setup-uv@v6.3.1
  with:
    version: "0.7.20"
    enable-cache: true

- name: Set up Python
  run: uv python install 3.13

- name: Restore uv cache
  uses: actions/cache@v4
  with:
    path: /tmp/.uv-cache
    key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
    restore-keys: |
      uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
      uv-${{ runner.os }}

- name: Install dependencies
  run: uv sync

- name: Minimize uv cache
  run: uv cache prune --ci
```

## Single Python Version Testing

```yaml
# Test on Python 3.13 (latest stable)
- name: Set up Python
  run: uv python install 3.13

- name: Run tests
  run: make test
```

## Security Workflow Pattern

### Comprehensive Security Scanning

```yaml
# .github/workflows/security.yml
name: Security

on:
  push:
    branches: [main, dev]
    paths:
      - '**.py'
      - 'pyproject.toml'
      - 'uv.lock'
      - 'requirements*.txt'
      - '.github/workflows/security.yml'
  pull_request:
    branches: [main, dev]
    paths:
      - '**.py'
      - 'pyproject.toml'
      - 'uv.lock'
      - 'requirements*.txt'
      - '.github/workflows/security.yml'
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday
  workflow_dispatch:

jobs:
  dependency-review:
    name: Dependency Review
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Dependency Review
        uses: actions/dependency-review-action@v4
        with:
          fail-on-severity: moderate
```

## Makefile CI Integration

### CI-Safe Command Patterns

```makefile
# CI-specific targets in Makefile
# Check code quality without making changes (CI-safe)
check-commit: check test
	@echo "Code quality check complete (no fixes applied)!"

# Security scanning
security:
	@echo "Running security scans..."
	uv add --dev pip-audit bandit
	uv run pip-audit --format=json --output=security-report.json
	uv run bandit -r . -f json -o bandit-report.json -x tests/,.venv/,personal_server.egg-info/ || true

# Quality workflow for CI
quality-ci: check-commit
	@echo "CI quality workflow completed successfully!"

# Local development commands (with auto-fixes)
fix:
	@echo "Formatting and fixing code..."
	uv run ruff format .
	uv run ruff check . --fix

# Test commands
test:
	@echo "Running tests..."
	uv run pytest

test-cov:
	@echo "Running tests with coverage..."
	uv run pytest --cov=. --cov-report=html --cov-report=term
```

## Path-Based Filtering Pattern

### Efficient Workflow Triggers

```yaml
# Only run workflows when relevant files change
paths:
  - '**.py'           # Python source files
  - 'pyproject.toml'  # Project configuration
  - 'uv.lock'         # Dependency lock file
  - 'Makefile'        # Build scripts
  - '.github/workflows/**'  # Workflow changes
```

## Artifact Management

### Test and Security Report Handling

```yaml
# Upload test and security reports
- name: Upload coverage reports
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: htmlcov/
    retention-days: 30

- name: Upload security reports
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: security-reports
    path: |
      security-report.json
      bandit-report.json
      semgrep-report.json
    retention-days: 30

# Upload test results
- name: Upload pytest results
  if: always()
  uses: actions/upload-artifact@v4
  with:
    name: pytest-results
    path: |
      test-results.xml
      coverage.xml
    retention-days: 30
```

## Dependabot Configuration

### Automated Dependency Management

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    reviewers:
      - "albertsikkema"
    assignees:
      - "albertsikkema"
    commit-message:
      prefix: "chore"
      include: "scope"

  # GitHub Actions updates
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    reviewers:
      - "albertsikkema"
    assignees:
      - "albertsikkema"
    commit-message:
      prefix: "ci"
      include: "scope"
```

## CI/CD Best Practices

### Performance Optimization Patterns

#### uv Caching Strategy
```yaml
# Efficient caching with proper cache keys
- name: Restore uv cache
  uses: actions/cache@v4
  with:
    path: /tmp/.uv-cache
    key: uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
    restore-keys: |
      uv-${{ runner.os }}-${{ hashFiles('uv.lock') }}
      uv-${{ runner.os }}
```

#### Path-Based Filtering
- Only run workflows on relevant file changes
- Parallel job execution for quality and security checks
- Smart cache invalidation based on lock file hash

### Security Integration Patterns

#### Multi-Tool Security Scanning
```yaml
# Comprehensive security workflow
jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      # Dependency vulnerability scanning
      - name: Run pip-audit
        run: |
          uv add --dev pip-audit
          uv run pip-audit --format=json --output=security-report.json
      
      # Code security scanning
      - name: Run bandit
        run: |
          uv add --dev bandit
          uv run bandit -r . -f json -o bandit-report.json -x tests/,.venv/ || true
      
      # SAST scanning with Semgrep
      - name: Run Semgrep
        uses: semgrep/semgrep-action@v1
        with:
          config: auto
          output: semgrep-report.json
```

#### Graceful Error Handling
```yaml
# Continue on non-critical errors
- name: Security scan (non-blocking)
  run: make security
  continue-on-error: true
```

### Development Workflow Patterns

#### CI-Safe Commands
- `make check-commit`: No auto-fixes in CI environment
- `make fix`: Auto-fixes for local development
- `make quality-ci`: CI-specific quality workflow

#### Local Development Parity
```bash
# Same commands work locally and in CI
make check-commit  # CI workflow
make quality       # Local development workflow
make test          # Universal test command
make test-cov      # Coverage testing
```

## Status Checks for Branch Protection

### Required Status Check Configuration

```yaml
# Recommended required status checks for branch protection
required_status_checks:
  strict: true
  contexts:
    - "Quality & Testing / Code Quality"
    - "Quality & Testing / Build Check"
    - "Security / Dependency Review"
    - "Security / Security Scan"

# Branch protection rules
branch_protection_rules:
  enforce_admins: false
  required_pull_request_reviews:
    required_approving_review_count: 1
    dismiss_stale_reviews: true
    require_code_owner_reviews: true
  restrictions: null
```

## Migration Benefits from pip to uv

### Performance Improvements
- **10-100x faster dependency resolution**: UV resolves 72 packages in milliseconds vs. minutes with pip
- **Better caching**: More efficient cache management with proper invalidation
- **Unified tooling**: Single tool for dependencies, virtual environments, and execution
- **Modern Python packaging**: Following 2025 best practices with pyproject.toml

### CI/CD Specific Benefits
```yaml
# Before (pip): 3-5 minutes for dependency installation
- name: Install dependencies (pip)
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    pip install -r requirements-dev.txt

# After (uv): 10-30 seconds for dependency installation
- name: Install dependencies (uv)
  run: uv sync
```

## Key Configuration Files

### Essential CI/CD Files
- `.github/workflows/quality.yml`: Main quality and testing workflow
- `.github/workflows/security.yml`: Security scanning workflow  
- `.github/dependabot.yml`: Dependency update configuration
- `Makefile`: CI/CD command definitions and local development commands
- `pyproject.toml`: Project configuration with uv dependencies
- `uv.lock`: Dependency lock file for reproducible builds

### Environment Variables
```yaml
# Common environment variables for CI/CD
env:
  UV_CACHE_DIR: /tmp/.uv-cache
  PYTHONPATH: ${{ github.workspace }}
  PYTHONDONTWRITEBYTECODE: 1
  PYTHONUNBUFFERED: 1
```

## Monitoring and Observability

### Workflow Monitoring
```yaml
# Add workflow monitoring
- name: Workflow telemetry
  uses: actions/github-script@v7
  with:
    script: |
      console.log('Workflow completed:', context.workflow);
      console.log('Job status:', context.job.status);
```

### Performance Metrics
```yaml
# Track build times
- name: Build performance
  run: |
    echo "Dependencies installed in: $(date)"
    echo "Tests completed in: $(date)"
```

This comprehensive CI/CD pipeline ensures fast, reliable, and secure automated testing and deployment processes.