"""
Pytest configuration and fixtures
"""
import pytest
import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def sample_grid_config():
    """Sample configuration for ray casting grid"""
    return {
        'rows': 10,
        'cols': 10,
        'square_pos': [5, 5],
        'square_size': 2,
        'light_pos': [1, 1]
    }


@pytest.fixture
def large_grid_config():
    """Large grid configuration for performance testing"""
    return {
        'rows': 50,
        'cols': 50,
        'square_pos': [25, 25],
        'square_size': 5,
        'light_pos': [5, 5]
    }
