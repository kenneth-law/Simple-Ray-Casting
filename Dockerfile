# Multi-stage build for Simple Ray Casting

# Stage 1: Base image with dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for tkinter
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    xvfb \
    x11-utils \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production image
FROM base as production

# Copy application code
COPY Main.py .
COPY CanvasRayTracer.py .
COPY RayCastTest.py .
COPY README.md .

# Create a non-root user
RUN useradd -m -u 1000 raycast && \
    chown -R raycast:raycast /app

USER raycast

# Set display for X11
ENV DISPLAY=:99

# Default command
CMD ["python", "Main.py"]

# Stage 3: Development image with testing tools
FROM base as development

# Copy all files including tests
COPY . .

# Install development dependencies
RUN pip install --no-cache-dir pytest pytest-cov flake8 black pylint mypy

# Run tests by default in dev mode
CMD ["pytest", "tests/", "-v"]

# Stage 4: Testing image
FROM development as test

# Run the test suite
RUN pytest tests/ -v --cov=. --cov-report=term

# Stage 5: Headless execution (for CI/CD)
FROM production as headless

# Install virtual framebuffer for headless execution
USER root
RUN apt-get update && apt-get install -y \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

USER raycast

# Use xvfb-run to provide virtual display
ENTRYPOINT ["xvfb-run", "-a"]
CMD ["python", "Main.py"]
