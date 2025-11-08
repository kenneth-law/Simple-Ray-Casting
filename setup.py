"""
Setup script for Simple Ray Casting
"""
from setuptools import setup, find_packages
import os

# Read the README for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    """Read requirements from requirements.txt, excluding dev dependencies"""
    requirements = []
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith("#"):
                    # Skip dev dependencies
                    if not any(pkg in line for pkg in ["pytest", "flake8", "black", "pylint", "mypy"]):
                        requirements.append(line)
    return requirements

setup(
    name="simple-ray-casting",
    version="1.0.0",
    author="Ray Casting Project",
    author_email="",
    description="Interactive ray casting visualization with shadows",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/kenneth-law/Simple-Ray-Casting",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "flake8>=6.0.0",
            "black>=23.0.0",
            "pylint>=2.17.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "raycast=Main:displayOut",
            "raycast-canvas=CanvasRayTracer:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
