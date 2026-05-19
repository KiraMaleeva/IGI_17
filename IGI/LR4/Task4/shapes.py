from abc import ABC, abstractmethod
from typing import Tuple
import math

class GeometricFigure(ABC):
    """
    Abstract base class for geometric figures
    """
    
    # Static attribute (class-level)
    figure_count = 0
    
    def __init__(self):
        GeometricFigure.figure_count += 1
    
    @abstractmethod
    def calculate_area(self) -> float:
        """Calculate area of the figure"""
        pass
    
    @abstractmethod
    def calculate_perimeter(self) -> float:
        """Calculate perimeter of the figure"""
        pass
    
    @classmethod
    def get_figure_count(cls) -> int:
        """Return total number of figures created"""
        return cls.figure_count


class DrawableMixin:
    """
    Mixin class for drawable figures
    """
    
    def get_vertices_for_drawing(self) -> list:
        """Return vertices coordinates for drawing"""
        raise NotImplementedError
    
    def get_center(self) -> Tuple[float, float]:
        """Return center point of the figure"""
        raise NotImplementedError