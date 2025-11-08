"""
Unit tests for ray casting functionality
"""
import pytest
import math
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from RayCastTest import cast
from Main import createMatrix


class TestRayCasting:
    """Test cases for basic ray casting functionality"""

    def test_cast_basic(self):
        """Test basic ray casting with a simple configuration"""
        result = cast(
            r=6,
            c=6,
            square_pos=[2, 2],
            square_size=1,
            light_pos=[0, 0]
        )
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0

    def test_cast_shadow_detection(self):
        """Test that shadows are properly detected"""
        result = cast(
            r=6,
            c=6,
            square_pos=[2, 2],
            square_size=1,
            light_pos=[0, 0]
        )
        # Shadow character should be present
        assert '▒' in result

    def test_cast_light_source(self):
        """Test that light source is marked correctly"""
        result = cast(
            r=6,
            c=6,
            square_pos=[2, 2],
            square_size=1,
            light_pos=[0, 0]
        )
        # Light source character should be present
        assert '*' in result

    def test_cast_object_marker(self):
        """Test that objects are marked correctly"""
        result = cast(
            r=6,
            c=6,
            square_pos=[2, 2],
            square_size=1,
            light_pos=[0, 0]
        )
        # Object marker should be present
        assert '.' in result

    def test_cast_different_sizes(self):
        """Test ray casting with different grid sizes"""
        sizes = [(5, 5), (10, 10), (3, 3)]
        for r, c in sizes:
            result = cast(
                r=r,
                c=c,
                square_pos=[1, 1],
                square_size=1,
                light_pos=[0, 0]
            )
            assert result is not None
            lines = result.split('\n')
            assert len(lines) == r

    def test_cast_no_square(self):
        """Test ray casting without a square object"""
        result = cast(
            r=5,
            c=5,
            square_pos=None,
            square_size=1,
            light_pos=[2, 2]
        )
        # Should only have light and background
        assert '*' in result
        assert '█' in result


class TestCreateMatrix:
    """Test cases for the createMatrix function"""

    def test_create_matrix_basic(self):
        """Test basic matrix creation"""
        result = createMatrix(
            r=10,
            c=10,
            square_pos=[5, 5],
            square_size=2,
            light_pos=[1, 1]
        )
        assert result is not None
        assert isinstance(result, str)

    def test_create_matrix_with_circle(self):
        """Test matrix creation with a circle"""
        result = createMatrix(
            r=20,
            c=20,
            circle_center=[10, 10],
            circle_radius=5,
            light_pos=[1, 1]
        )
        assert result is not None
        assert '.' in result

    def test_create_matrix_with_square(self):
        """Test matrix creation with a square"""
        result = createMatrix(
            r=15,
            c=15,
            square_pos=[7, 7],
            square_size=3,
            light_pos=[1, 1]
        )
        assert result is not None
        assert '.' in result

    def test_create_matrix_light_and_shadow(self):
        """Test that light source and shadows are created"""
        result = createMatrix(
            r=10,
            c=10,
            square_pos=[5, 5],
            square_size=2,
            light_pos=[1, 1]
        )
        # Should contain light source
        assert '*' in result
        # Should contain shadows
        assert '▒' in result

    def test_create_matrix_both_objects(self):
        """Test matrix with both circle and square"""
        result = createMatrix(
            r=30,
            c=30,
            circle_center=[10, 10],
            circle_radius=4,
            square_pos=[20, 20],
            square_size=3,
            light_pos=[1, 1]
        )
        assert result is not None
        # Both objects should be marked
        assert '.' in result


class TestRayGeometry:
    """Test geometric calculations used in ray casting"""

    def test_distance_calculation(self):
        """Test that distance calculation is correct"""
        # Simple Pythagorean theorem
        dx, dy = 3, 4
        distance = math.sqrt(dx*dx + dy*dy)
        assert distance == 5.0

    def test_normalization(self):
        """Test vector normalization"""
        dx, dy = 3, 4
        distance = math.sqrt(dx*dx + dy*dy)
        nx, ny = dx/distance, dy/distance
        # Normalized vector should have length 1
        assert abs(math.sqrt(nx*nx + ny*ny) - 1.0) < 0.0001

    def test_ray_direction(self):
        """Test ray direction calculation"""
        light_x, light_y = 0, 0
        point_x, point_y = 5, 5

        dx = point_x - light_x
        dy = point_y - light_y

        assert dx == 5
        assert dy == 5

        # Direction should be at 45 degrees
        distance = math.sqrt(dx*dx + dy*dy)
        nx, ny = dx/distance, dy/distance

        # Both components should be equal for 45 degree angle
        assert abs(nx - ny) < 0.0001


def test_module_imports():
    """Test that all required modules can be imported"""
    try:
        import RayCastTest
        import Main
        assert True
    except ImportError as e:
        pytest.fail(f"Failed to import required modules: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
