import math
from typing import List, Dict


class CosSeries:
    """Class for analyzing cos(x) and its Taylor series."""
    
    @staticmethod
    def math_cos(x: float) -> float:
        """Calculate cos(x) using math library."""
        return math.cos(x)
    
    @staticmethod
    def taylor_cos(x: float, n_terms: int) -> float:
        """
        Taylor series for cos(x): 1 - x^2/2! + x^4/4! - x^6/6! + ...
        """
        result = 0.0
        for i in range(n_terms):
            sign = (-1) ** i
            power = 2 * i
            term = sign * (x ** power) / math.factorial(power)
            result += term
        return result
    
    def generate_plot_data(self, x_start: float, x_end: float, 
                           num_points: int, terms_list: List[int]) -> List[Dict]:
        """Generate data for plotting."""
        data = []
        step = (x_end - x_start) / (num_points - 1)
        
        for n_terms in terms_list:
            for i in range(num_points):
                x = x_start + i * step
                data.append({
                    'x': x,
                    'series_value': self.taylor_cos(x, n_terms),
                    'math_value': self.math_cos(x),
                    'n_terms': n_terms
                })
        return data