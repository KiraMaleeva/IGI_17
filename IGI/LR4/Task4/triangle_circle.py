from shapes import GeometricFigure, DrawableMixin
from color import FigureColor
import math
from typing import Tuple, List

class InscribedTriangle(GeometricFigure, DrawableMixin):
    """
    Equilateral triangle inscribed in a circle
    Inherits from GeometricFigure and uses DrawableMixin
    """
    
    # Static attribute - figure type name
    figure_type = "Equilateral Triangle (inscribed in circle)"
    
    def __init__(self, radius: float, color: str):
        """
        Constructor
        
        Args:
            radius: Radius of circumscribed circle
            color: Color of the triangle
        """
        super().__init__()
        self._radius = radius
        self._color_obj = FigureColor(color)
        self._side_length = self._calculate_side()
    
    def _calculate_side(self) -> float:
        """Calculate side length of inscribed equilateral triangle"""
        # For equilateral triangle inscribed in circle: side = R * √3
        return self._radius * math.sqrt(3)
    
    def calculate_area(self) -> float:
        """Calculate area of equilateral triangle"""
        return (math.sqrt(3) / 4) * (self._side_length ** 2)
    
    def calculate_perimeter(self) -> float:
        """Calculate perimeter of triangle"""
        return 3 * self._side_length
    
    def get_vertices_for_drawing(self) -> List[Tuple[float, float]]:
        """Get triangle vertices coordinates"""
        vertices = []
        for i in range(3):
            angle = math.radians(90 + i * 120)  # Start from top
            x = self._radius * math.cos(angle)
            y = self._radius * math.sin(angle)
            vertices.append((x, y))
        return vertices
    
    def get_center(self) -> Tuple[float, float]:
        """Get center of circumscribed circle"""
        return (0, 0)
    
    def get_circle_points(self) -> List[Tuple[float, float]]:
        """Get points for drawing circumscribed circle"""
        points = []
        for i in range(100):
            angle = 2 * math.pi * i / 100
            x = self._radius * math.cos(angle)
            y = self._radius * math.sin(angle)
            points.append((x, y))
        return points
    
    def get_info(self) -> str:
        """Get formatted information about the triangle"""
        return (
            f"Circumscribed circle radius: {self._radius:.2f}\n"
            f"Triangle side length: {self._side_length:.2f}\n"
            f"Area: {self.calculate_area():.2f} sq units\n"
            f"Perimeter: {self.calculate_perimeter():.2f} units\n"
            f"Color: {self._color_obj.color}\n"
        )
    
    def __str__(self) -> str:
        """Magic method for string representation"""
        return f"InscribedTriangle(R={self._radius}, color={self._color_obj.color})"
    
    def __repr__(self) -> str:
        """Magic method for representation"""
        return f"InscribedTriangle({self._radius}, '{self._color_obj.color}')"