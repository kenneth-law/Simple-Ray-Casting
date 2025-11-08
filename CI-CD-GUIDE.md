# CI/CD Pipeline Guide

This document explains the CI/CD setup for the Simple Ray Casting project.

## Overview

The project uses **GitHub Actions** for continuous integration and deployment, with support for:
- Automated testing across multiple Python versions
- Code quality checks (linting, formatting, type checking)
- Docker image building
- Package building and distribution
- Automated releases

## Pipeline Structure

### 1. Test Job (`test`)

Runs on every push and pull request to main branches.

**Matrix Testing:**
- Python versions: 3.8, 3.9, 3.10, 3.11
- OS: Ubuntu Latest

**Steps:**
1. Checkout code
2. Set up Python environment
3. Install dependencies (with caching)
4. Run flake8 linting
5. Check code formatting with black
6. Run pytest with coverage
7. Upload coverage to Codecov

**Local Execution:**
```bash
make test          # Run tests
make test-cov      # Run tests with coverage report
```

### 2. Code Quality Job (`code-quality`)

Performs static analysis and type checking.

**Tools:**
- **pylint**: Code quality and style checking
- **mypy**: Static type checking

**Local Execution:**
```bash
make lint-all      # Run all linting tools
```

### 3. Build Job (`build`)

Creates distributable Python packages.

**Outputs:**
- Source distribution (`.tar.gz`)
- Wheel distribution (`.whl`)

**Local Execution:**
```bash
make build         # Build Python package
```

### 4. Docker Job (`docker`)

Builds and optionally pushes Docker images.

**Triggers:**
- Only on push to main/master branches

**Features:**
- Multi-stage Docker builds
- Image caching with GitHub Actions cache
- Metadata extraction for proper tagging

**Local Execution:**
```bash
make docker-build  # Build Docker image
make docker-run    # Run in Docker
make docker-test   # Test in Docker
```

### 5. Release Job (`release`)

Creates GitHub releases with artifacts.

**Triggers:**
- Only on version tags (e.g., `v1.0.0`)

**Artifacts:**
- Python packages
- Docker images

## Using the Makefile

The project includes a Makefile for common development tasks:

```bash
# Development
make install       # Install dependencies
make install-dev   # Install dev dependencies

# Testing
make test          # Run tests
make test-cov      # Run tests with coverage

# Code Quality
make lint          # Run flake8
make lint-all      # Run all linting tools
make format        # Format code with black
make format-check  # Check formatting

# Building
make build         # Build Python package
make clean         # Clean build artifacts

# Docker
make docker-build  # Build Docker images
make docker-run    # Run application
make docker-test   # Run tests in Docker
make docker-dev    # Development environment

# CI Simulation
make ci            # Run complete CI pipeline locally
make all           # Format, lint, and test
```

## Docker Deployment

### Multi-Stage Builds

The Dockerfile provides multiple build targets:

1. **base**: Base image with dependencies
2. **production**: Minimal production image
3. **development**: Full development environment
4. **test**: Testing environment
5. **headless**: For CI/CD (with virtual display)

### Using Docker Compose

```bash
# Production
docker-compose up raycast

# Development (with hot reload)
docker-compose up raycast-dev

# Testing
docker-compose up raycast-test

# Headless (CI/CD)
docker-compose up raycast-headless
```

## Setting Up CI/CD

### GitHub Actions Setup

The workflow is automatically triggered on:
- Push to `main`, `master`, `develop`, or `claude/**` branches
- Pull requests to `main`, `master`, `develop`
- Manual workflow dispatch

### Required Secrets (Optional)

For Docker Hub integration:
- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password/token

Add these in: Repository Settings → Secrets and variables → Actions

### Branch Protection (Recommended)

1. Go to Repository Settings → Branches
2. Add rule for `main` branch:
   - Require status checks to pass
   - Require branches to be up to date
   - Include: `test`, `code-quality`, `build`

## Creating a Release

1. Update version in `setup.py` and `pyproject.toml`
2. Commit changes
3. Create and push a tag:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```
4. GitHub Actions will automatically:
   - Run all tests
   - Build packages
   - Create a GitHub release
   - Upload artifacts

## Continuous Deployment Options

### Option 1: PyPI Publishing

Add to `.github/workflows/ci-cd.yml`:

```yaml
- name: Publish to PyPI
  if: startsWith(github.ref, 'refs/tags/v')
  env:
    TWINE_USERNAME: __token__
    TWINE_PASSWORD: ${{ secrets.PYPI_TOKEN }}
  run: |
    pip install twine
    twine upload dist/*
```

### Option 2: Docker Hub Publishing

Already configured! Just add secrets:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

### Option 3: GitHub Packages

Modify the docker job to use `ghcr.io`:

```yaml
- name: Log in to GitHub Container Registry
  uses: docker/login-action@v3
  with:
    registry: ghcr.io
    username: ${{ github.actor }}
    password: ${{ secrets.GITHUB_TOKEN }}
```

## Local Development Workflow

1. **Clone repository**
   ```bash
   git clone <repo-url>
   cd Simple-Ray-Casting
   ```

2. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   make install-dev
   ```

3. **Make changes and test**
   ```bash
   make format      # Format code
   make lint        # Check code quality
   make test        # Run tests
   ```

4. **Run locally**
   ```bash
   python Main.py
   # or
   python CanvasRayTracer.py
   ```

5. **Commit and push**
   ```bash
   git add .
   git commit -m "Your changes"
   git push
   ```

6. **Watch CI pipeline**
   - Go to Actions tab in GitHub
   - Monitor workflow execution

## Troubleshooting

### Tests failing in CI but passing locally

- Ensure you're testing with the same Python version
- Check for missing dependencies in `requirements.txt`
- Look for OS-specific issues (tkinter on Linux)

### Docker build failing

- Check Dockerfile syntax
- Ensure all files exist
- Verify `.dockerignore` isn't excluding necessary files

### Coverage reports not uploading

- Verify Codecov integration
- Check if `coverage.xml` is generated
- Ensure network connectivity

## Performance Optimization

### Caching

The pipeline uses caching for:
- Pip dependencies
- Docker layers
- GitHub Actions cache

### Parallel Execution

Tests run in parallel across Python versions using matrix strategy.

### Resource Usage

Approximate CI times:
- Test job: 2-3 minutes per Python version
- Code quality: 1-2 minutes
- Build: 1-2 minutes
- Docker: 3-5 minutes

## Best Practices

1. **Always run tests locally** before pushing
2. **Use feature branches** for development
3. **Keep dependencies updated** regularly
4. **Monitor CI pipeline** after each push
5. **Use semantic versioning** for releases
6. **Document breaking changes** in commits
7. **Review coverage reports** to maintain quality

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [pytest Documentation](https://docs.pytest.org/)
- [Python Packaging Guide](https://packaging.python.org/)
