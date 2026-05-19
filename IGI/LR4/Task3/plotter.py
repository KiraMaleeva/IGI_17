import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict


class FunctionPlotter:
    """Class for plotting cos(x) and its Taylor series."""
    
    def __init__(self):
        self.fig = None
        self.ax = None
    
    def setup_plot(self, x_start: float = -2*np.pi, x_end: float = 2*np.pi):
        """Setup plot with axes, grid, labels."""
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.ax.set_title("cos(x): Math Function vs Taylor Series", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("x (radians)", fontsize=12)
        self.ax.set_ylabel("cos(x)", fontsize=12)
        self.ax.grid(True, alpha=0.3)
        self.ax.axhline(y=0, color='k', linewidth=0.5)   # X-axis
        self.ax.axvline(x=0, color='k', linewidth=0.5)   # Y-axis
        self.ax.set_xlim(x_start, x_end)
        self.ax.set_ylim(-1.5, 1.5)
    
    def plot_comparison(self, data: List[Dict]):
        """Plot math function and Taylor series with different colors."""
        series_by_terms = {}
        math_points = {}
        
        for point in data:
            x = point['x']
            n_terms = point['n_terms']
            
            if x not in math_points:
                math_points[x] = point['math_value']
            
            if n_terms not in series_by_terms:
                series_by_terms[n_terms] = {'x': [], 'y': []}
            series_by_terms[n_terms]['x'].append(x)
            series_by_terms[n_terms]['y'].append(point['series_value'])
        
        # Math function (blue solid) - график из модуля math
        x_math = sorted(math_points.keys())
        y_math = [math_points[x] for x in x_math]
        self.ax.plot(x_math, y_math, 'b-', label='math.cos(x)', linewidth=2)
        
        # Taylor series (разные цвета, пунктирные)
        colors = ['red', 'green', 'orange', 'purple', 'brown']
        for i, (n_terms, points) in enumerate(sorted(series_by_terms.items())):
            color = colors[i % len(colors)]
            self.ax.plot(points['x'], points['y'], 
                        color=color, linestyle='--', marker='o',
                        label=f'Series (n={n_terms})', linewidth=1.5, markersize=2)
    
    def add_legend(self):
        """Add legend."""
        self.ax.legend(loc='best', fontsize=10)
    
    def add_annotations(self):
        """Add text annotations."""
        self.ax.annotate('cos(0) = 1', xy=(0, 1), xytext=(0.5, 1.1),
                        arrowprops=dict(arrowstyle='->', color='gray'))
        self.ax.annotate('cos(π) = -1', xy=(np.pi, -1), xytext=(np.pi + 0.5, -0.8),
                        arrowprops=dict(arrowstyle='->', color='gray'))
        self.ax.text(-5.5, 0.8, 'Taylor series converges to cos(x)', fontsize=9,
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
    
    def save_plot(self, filename: str = 'cos_series_plot.png'):
        """Save plot to file (part c)."""
        plt.tight_layout()
        plt.savefig(filename, dpi=300)
    
    def show_plot(self):
        """Display plot."""
        plt.show()
    
    def close(self):
        """Close plot."""
        plt.close(self.fig)