.PHONY: help install test lint format clean build docker-build docker-run docker-test all

# Default target
help:
	@echo "Simple Ray Casting - Makefile Commands"
	@echo "======================================"
	@echo "install       - Install dependencies"
	@echo "install-dev   - Install development dependencies"
	@echo "test          - Run tests with pytest"
	@echo "test-cov      - Run tests with coverage report"
	@echo "lint          - Run linting (flake8)"
	@echo "lint-all      - Run all linting tools (flake8, pylint, mypy)"
	@echo "format        - Format code with black"
	@echo "format-check  - Check code formatting without modifying"
	@echo "clean         - Remove build artifacts and cache files"
	@echo "build         - Build Python package"
	@echo "docker-build  - Build Docker image"
	@echo "docker-run    - Run application in Docker"
	@echo "docker-test   - Run tests in Docker"
	@echo "docker-dev    - Run development environment in Docker"
	@echo "all           - Run format, lint, and test"

# Install production dependencies
install:
	pip install -r requirements.txt

# Install development dependencies
install-dev:
	pip install -r requirements.txt
	pip install -e .[dev]

# Run tests
test:
	pytest tests/ -v

# Run tests with coverage
test-cov:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

# Lint with flake8
lint:
	flake8 *.py --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=tests,venv,.git,__pycache__
	flake8 *.py --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics --exclude=tests,venv,.git,__pycache__

# Run all linting tools
lint-all: lint
	pylint *.py --exit-zero --disable=C0114,C0115,C0116 --max-line-length=127
	mypy *.py --ignore-missing-imports --no-strict-optional

# Format code with black
format:
	black *.py --extend-exclude="/(\.git|\.venv|venv|__pycache__)/"

# Check formatting without modifying
format-check:
	black --check --diff *.py --extend-exclude="/(\.git|\.venv|venv|__pycache__)/"

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete

# Build package
build: clean
	python -m build

# Build Docker image
docker-build:
	docker-compose build

# Run application in Docker
docker-run:
	docker-compose up raycast

# Run tests in Docker
docker-test:
	docker-compose run --rm raycast-test

# Run development environment
docker-dev:
	docker-compose up raycast-dev

# Run all quality checks
all: format lint test

# CI pipeline simulation
ci: format-check lint-all test-cov
	@echo "CI pipeline completed successfully!"
