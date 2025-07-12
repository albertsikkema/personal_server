# PRP: GitHub Actions Quality Workflow Implementation

## Feature: Setup a GitHub workflow that runs `make quality` on every PR and commit

### Overview
Implement a comprehensive GitHub Actions CI/CD workflow that automatically runs code quality checks on every pull request and commit. The workflow will leverage the existing `make quality` command while following modern 2025 best practices for Python projects using uv, FastAPI, and GitHub Actions.

### Context & Documentation

#### GitHub Actions Best Practices (2025)
- **Official Documentation**: https://docs.github.com/en/actions/learn-github-actions/understanding-github-actions
- **Workflow Syntax**: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
- **Python CI/CD Guide**: https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python
- **Security Best Practices**: https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions

#### uv Integration with GitHub Actions
- **uv GitHub Integration**: https://docs.astral.sh/uv/guides/integration/github/
- **setup-uv Action**: https://github.com/astral-sh/setup-uv
- **uv FastAPI Example**: https://github.com/astral-sh/uv-fastapi-example

#### Key Benefits of Modern CI/CD (2025)
1. **10-100x Speed Improvement**: uv provides dramatically faster dependency resolution
2. **Intelligent Caching**: Path-based triggers and dependency caching reduce unnecessary runs
3. **Security**: Proper handling of pull requests from forks and dependency vulnerabilities
4. **Developer Experience**: Consistent interface between local development and CI

### Existing Codebase Analysis

#### Current Make Quality Commands (Makefile:71-90)
```makefile
# Complete code quality workflow (with fixes)
quality: fix test
	@echo "Code quality check complete!"

# Check code quality without making changes (CI-safe)
check-commit: check test
	@echo "Code quality check complete (no fixes applied)!"
```

**Key difference:**
- `quality` target: Runs `fix` (applies auto-fixes) then `test`
- `check-commit` target: Runs `check` (analysis only) then `test`

Where:
- `fix` target: `uv run ruff check --fix .` and `uv run ruff format .`
- `check` target: `uv run ruff check .` and `uv run ruff format --check .`
- `test` target: `uv run pytest`

#### Project Structure & Dependencies
- **Package Manager**: uv (modern Python package manager)
- **Framework**: FastAPI with API key authentication
- **Testing**: pytest with fixtures and coverage
- **Linting**: ruff (modern replacement for flake8, black, isort)
- **Python Version**: 3.10+ (requires-python = ">=3.10"), default 3.13

#### Existing CI/CD Status
- **No existing workflows**: `.github/workflows/` directory does not exist
- **Ready for CI**: Project has comprehensive testing suite (160+ tests)
- **Quality tooling**: All quality tools properly configured in pyproject.toml

### Implementation Blueprint

#### 1. Directory Structure
```
.github/
└── workflows/
    ├── quality.yml          # Main quality workflow (code quality, tests)
    └── security.yml         # Security scanning (vulnerabilities, code security)
```

#### 2. Main Quality Workflow
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
      docs: ${{ steps.changes.outputs.docs }}
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
            docs:
              - 'README.md'
              - 'PRPs/**'
              - 'ai_info/**'

  quality:
    name: Code Quality
    runs-on: ubuntu-latest
    needs: changes
    if: ${{ needs.changes.outputs.python == 'true' }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          version: "0.8.0"
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
      
      - name: Run make check-commit
        run: make check-commit
      
      - name: Upload coverage reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/
          retention-days: 30
      
      - name: Minimize uv cache
        run: uv cache prune --ci

  test-matrix:
    name: Test Matrix
    runs-on: ubuntu-latest
    needs: changes
    if: ${{ needs.changes.outputs.python == 'true' }}
    
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          version: "0.8.0"
          enable-cache: true
      
      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: uv sync
      
      - name: Run tests
        run: make test
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}
          files: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
          fail_ci_if_error: false

  build-check:
    name: Build Check
    runs-on: ubuntu-latest
    needs: [quality, test-matrix]
    if: ${{ needs.changes.outputs.python == 'true' }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          version: "0.8.0"
      
      - name: Set up Python
        run: uv python install 3.13
      
      - name: Install dependencies
        run: uv sync
      
      - name: Test application startup
        run: |
          uv run python -c "from main import app; print('✅ Application imports successfully')"
      
      - name: Run development server test
        run: |
          timeout 10s uv run uvicorn main:app --host 0.0.0.0 --port 8000 &
          sleep 5
          curl -f http://localhost:8000/health || exit 1
          echo "✅ Development server starts successfully"
```

#### 3. Security Workflow (Separate from Quality)
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

env:
  UV_CACHE_DIR: /tmp/.uv-cache

jobs:
  changes:
    name: Detect Security Changes
    runs-on: ubuntu-latest
    outputs:
      security: ${{ steps.changes.outputs.security }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: changes
        with:
          filters: |
            security:
              - '**.py'
              - 'pyproject.toml'
              - 'uv.lock'
              - 'requirements*.txt'
              - '.github/workflows/security.yml'

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

  security-scan:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: changes
    if: ${{ needs.changes.outputs.security == 'true' || github.event_name == 'schedule' }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          version: "0.8.0"
          enable-cache: true
      
      - name: Set up Python
        run: uv python install 3.13
      
      - name: Restore uv cache
        uses: actions/cache@v4
        with:
          path: /tmp/.uv-cache
          key: uv-security-${{ runner.os }}-${{ hashFiles('uv.lock') }}
          restore-keys: |
            uv-security-${{ runner.os }}-${{ hashFiles('uv.lock') }}
            uv-security-${{ runner.os }}
      
      - name: Install dependencies
        run: uv sync
      
      - name: Run security scan
        run: make security
      
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
      
      - name: Minimize uv cache
        run: uv cache prune --ci

  vulnerability-scan:
    name: Vulnerability Scan
    runs-on: ubuntu-latest
    needs: changes
    if: ${{ needs.changes.outputs.security == 'true' || github.event_name == 'schedule' }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          version: "0.8.0"
      
      - name: Set up Python
        run: uv python install 3.13
      
      - name: Install dependencies
        run: uv sync
      
      - name: Run vulnerability scan
        run: |
          uv add --dev safety
          uv run safety check --json --output vulnerability-report.json
        continue-on-error: true
      
      - name: Upload vulnerability report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: vulnerability-report
          path: vulnerability-report.json
          retention-days: 30

  code-security-scan:
    name: Code Security Scan
    runs-on: ubuntu-latest
    needs: changes
    if: ${{ needs.changes.outputs.security == 'true' || github.event_name == 'schedule' }}
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v6
        with:
          version: "0.8.0"
      
      - name: Set up Python
        run: uv python install 3.13
      
      - name: Install dependencies
        run: uv sync
      
      - name: Run code security scan
        run: |
          uv add --dev bandit semgrep
          uv run bandit -r . -f json -o bandit-report.json -x tests/
          uv run semgrep --config=auto --json --output=semgrep-report.json
        continue-on-error: true
      
      - name: Upload code security reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: code-security-reports
          path: |
            bandit-report.json
            semgrep-report.json
          retention-days: 30
```

#### 4. Makefile Enhancements
```makefile
# Add to existing Makefile
# CI-specific targets
ci-install:
	@echo "Installing dependencies for CI..."
	uv sync

ci-quality: ci-install
	@echo "Running CI quality checks..."
	uv run ruff check --output-format=github .
	uv run ruff format --check .
	uv run pytest --cov=. --cov-report=xml --cov-report=html

# Alias for check-commit (CI-safe)
ci-check-commit: check-commit

ci-test: ci-install
	@echo "Running CI tests..."
	uv run pytest -v --cov=. --cov-report=term-missing

# Security scanning
security:
	@echo "Running security scans..."
	uv add --dev safety bandit semgrep
	uv run safety check --json --output security-report.json
	uv run bandit -r . -f json -o bandit-report.json -x tests/
	uv run semgrep --config=auto --json --output=semgrep-report.json

# Build verification
build-check:
	@echo "Checking application build..."
	uv run python -c "from main import app; print('✅ Application imports successfully')"
```

### Advanced Features

#### 1. Branch Protection Rules
```yaml
# Suggested branch protection rules for main/dev branches
required_status_checks:
  strict: true
  contexts:
    - "Quality & Testing / Code Quality"
    - "Quality & Testing / Test Matrix (3.11)"
    - "Quality & Testing / Test Matrix (3.12)"
    - "Quality & Testing / Test Matrix (3.13)"
    - "Quality & Testing / Build Check"

enforce_admins: true
required_pull_request_reviews:
  required_approving_review_count: 1
  dismiss_stale_reviews: true
  require_code_owner_reviews: true

restrictions:
  users: []
  teams: []
  apps: []
```

#### 2. Dependabot Configuration
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
```

#### 3. Issue Templates
```yaml
# .github/ISSUE_TEMPLATE/bug_report.yml
name: Bug Report
description: File a bug report
title: "[Bug]: "
labels: ["bug", "triage"]
body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!
  
  - type: input
    id: contact
    attributes:
      label: Contact Details
      description: How can we get in touch with you if we need more info?
      placeholder: ex. email@example.com
    validations:
      required: false
  
  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: Also tell us, what did you expect to happen?
      placeholder: Tell us what you see!
    validations:
      required: true
  
  - type: dropdown
    id: version
    attributes:
      label: Version
      description: What version of the application are you running?
      options:
        - main (latest)
        - dev
        - feature branch
    validations:
      required: true
```

### Implementation Tasks

#### Phase 1: Core Workflow Setup
1. **Create GitHub Actions directory structure**
   - Create `.github/workflows/` directory
   - Create `quality.yml` workflow file
   - Test workflow with simple echo commands

2. **Implement basic quality workflow**
   - Add uv setup and Python installation
   - Add dependency caching
   - Add `make quality` execution
   - Test with a simple PR

#### Phase 2: Enhanced Testing
3. **Add matrix testing**
   - Configure Python version matrix (3.11, 3.12, 3.13)
   - Add proper test reporting
   - Add coverage reporting

4. **Create security workflow**
   - Create separate `security.yml` workflow
   - Configure security scanning with safety, bandit, semgrep
   - Add dependency review for pull requests

#### Phase 3: Optimization & Polish
5. **Add performance optimizations**
   - Implement path-based filtering
   - Add intelligent caching strategies
   - Configure parallel job execution

6. **Add repository protection**
   - Configure branch protection rules
   - Set up required status checks
   - Configure Dependabot

#### Phase 4: Documentation & Monitoring
7. **Update documentation**
   - Add workflow documentation to README.md
   - Update Claude.md with CI/CD patterns
   - Create contributor guidelines

8. **Add monitoring & notifications**
   - Configure failure notifications
   - Add status badges
   - Set up metrics collection

### Validation Gates

```bash
# Local validation before push (with fixes)
make quality

# CI-safe validation (no fixes applied)
make check-commit

# Test workflow locally (using act)
act push

# Validate YAML syntax
yamllint .github/workflows/quality.yml

# Test makefile targets
make ci-quality
make ci-test
make security
make build-check
```

### Error Handling Strategy

#### 1. Graceful Failure Handling
- Use `continue-on-error: true` for non-critical security scans
- Implement proper exit codes in make targets
- Add retry logic for flaky network operations

#### 2. Notification Strategy
- Configure GitHub notifications for workflow failures
- Add status badges to README.md
- Set up email notifications for critical failures

#### 3. Rollback Strategy
- Use `fail-fast: false` in matrix builds
- Implement workflow cancellation for outdated runs
- Add manual workflow triggers for debugging

### Success Criteria

#### Core Requirements
- [ ] **Workflow runs on every PR and commit to main/dev**
- [ ] **`make check-commit` executes successfully in CI (no fixes applied)**
- [ ] **All tests pass in CI environment**
- [ ] **Workflow completes in under 5 minutes**
- [ ] **Path-based filtering prevents unnecessary runs**

#### Advanced Features
- [ ] **Matrix testing across Python versions works**
- [ ] **Security workflow runs separately from quality workflow**
- [ ] **Security scanning reports vulnerabilities (safety, bandit, semgrep)**
- [ ] **Branch protection rules enforce quality checks**
- [ ] **Dependabot keeps dependencies updated**
- [ ] **Coverage reporting tracks test coverage**

#### Performance & Reliability
- [ ] **uv caching reduces build times by 50%+**
- [ ] **Parallel jobs execute efficiently**
- [ ] **Workflow artifacts are properly stored**
- [ ] **Error handling prevents false negatives**
- [ ] **Status checks integrate with PR reviews**

### Gotchas & Considerations

#### 1. GitHub Actions Limitations
- **Free tier limits**: 2,000 minutes/month for private repos
- **Concurrent job limits**: 5 concurrent jobs on free tier
- **Runner specifications**: Limited CPU/memory on free runners

#### 2. uv Integration Challenges
- **Cache invalidation**: Ensure proper uv cache management
- **Version pinning**: Pin uv version for reproducible builds
- **Platform differences**: Consider OS-specific behavior

#### 3. Security Considerations
- **Secrets management**: Never expose API keys in workflows
- **Fork PRs**: Use `pull_request_target` carefully
- **Dependency scanning**: Regular security updates required

#### 4. Performance Optimization
- **Path filtering**: Only run on relevant file changes
- **Caching strategy**: Balance cache size vs speed
- **Parallel execution**: Optimize job dependencies

### Repository Integration

#### 1. Branch Strategy Integration
```yaml
# Adapt to project's branching strategy
branches: [main, dev]  # Main development branches
paths:                 # Only run on relevant changes
  - '**.py'
  - 'pyproject.toml'
  - 'uv.lock'
```

#### 2. Conventional Commits Integration
- Use conventional commit types for automated changelog
- Configure semantic release for version management
- Add commit linting to prevent bad commit messages

#### 3. Existing Tools Integration
- Leverage existing make targets for consistency
- Reuse existing test configuration
- Maintain compatibility with local development

### 🎯 **CONFIDENCE SCORE: 9/10**

**HIGH CONFIDENCE DUE TO:**
- ✅ **Comprehensive Research**: Analyzed existing codebase, modern GitHub Actions patterns, and uv integration
- ✅ **Proven Technologies**: Using established tools (uv, ruff, pytest) with official GitHub Actions
- ✅ **Incremental Implementation**: Phased approach reduces risk of implementation issues
- ✅ **Existing Foundation**: Project already has robust testing and quality tooling
- ✅ **Modern Best Practices**: Following 2025 CI/CD best practices with security and performance optimization

**RISK MITIGATION:**
- ✅ **Path-based filtering** prevents unnecessary workflow runs
- ✅ **Caching strategies** minimize build times and cost
- ✅ **Security scanning** identifies vulnerabilities early
- ✅ **Matrix testing** ensures compatibility across Python versions
- ✅ **Comprehensive error handling** prevents false negatives

**EXPECTED OUTCOMES:**
- ✅ **10-100x faster dependency resolution** with uv
- ✅ **Consistent quality checks** on every PR and commit (CI-safe with no automatic fixes)
- ✅ **Separate security workflow** for comprehensive vulnerability scanning
- ✅ **Improved developer experience** with fast feedback loops
- ✅ **Professional CI/CD pipeline** following industry standards

The implementation leverages the new `make check-commit` command (CI-safe, no auto-fixes) for quality checks while using a separate security workflow for comprehensive vulnerability scanning with safety, bandit, and semgrep.