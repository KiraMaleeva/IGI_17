import matplotlib.pyplot as plt
import matplotlib.patches as patches
from typing import List, Tuple
import os

class FigureVisualizer:
    """
    Class for drawing geometric figures
    """
    
    def __init__(self):
        self.fig = None
        self.ax = None
    
    def setup_canvas(self, title: str = "Geometric Figure"):
        """Setup drawing canvas"""
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.ax.set_title(title, fontsize=14, fontweight='bold')
        self.ax.set_xlabel("X axis", fontsize=10)
        self.ax.set_ylabel("Y axis", fontsize=10)
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=0, color='k', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linewidth=0.5)
        self.ax.set_aspect('equal')
    
    def draw_triangle(self, vertices: List[Tuple[float, float]], 
                      color: str, alpha: float = 0.6,
                      edge_color: str = 'black'):
        """
        Draw triangle from vertices
        
        Args:
            vertices: List of (x, y) tuples
            color: Fill color
            alpha: Transparency (0-1)
            edge_color: Border color
        """
        if len(vertices) != 3:
            raise ValueError("Triangle requires exactly 3 vertices")
        
        # Close the polygon by adding first vertex at end
        x_coords = [v[0] for v in vertices] + [vertices[0][0]]
        y_coords = [v[1] for v in vertices] + [vertices[0][1]]
        
        self.ax.fill(x_coords, y_coords, color=color, alpha=alpha, 
                     edgecolor=edge_color, linewidth=2)
        
        # Mark vertices
        for x, y in vertices:
            self.ax.plot(x, y, 'ro', markersize=6)
            self.ax.annotate(f'({x:.2f}, {y:.2f})', 
                            (x, y), xytext=(5, 5),
                            textcoords='offset points', fontsize=8)
    
    def draw_circle(self, center: Tuple[float, float], radius: float,
                    color: str = 'gray', alpha: float = 0.3,
                    linestyle: str = '--'):
        """Draw circle (for circumscribed circle)"""
        circle = patches.Circle(center, radius, 
                                fill=False, color=color, 
                                linestyle=linestyle, linewidth=1.5)
        self.ax.add_patch(circle)
    
    def draw_axes_labels(self):
        """Draw axes labels and limits"""
        self.ax.set_xlim(-1.5, 1.5)
        self.ax.set_ylim(-1.5, 1.5)
    
    def add_text_label(self, text: str, position: Tuple[float, float],
                      fontsize: int = 10, bbox: bool = True):
        """Add text label to figure"""
        bbox_props = dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7) if bbox else None
        self.ax.text(position[0], position[1], text, fontsize=fontsize,
                    bbox=bbox_props, ha='center')
    
    def save_figure(self, filename: str = 'triangle_figure.png', dpi: int = 300):
        """Save figure to file"""
        plt.tight_layout()
        self.fig.savefig(filename, dpi=dpi, bbox_inches='tight')
    
    def show_figure(self):
        """Display the figure"""
        plt.show()
    
    def close(self):
        """Close the figure"""
        plt.close(self.fig)