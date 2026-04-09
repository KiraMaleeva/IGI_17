"""
Program to calculate cos(x) using power series expansion.
Lab Work 3, Task 1, Variant 17
Version: 1.0
Developer: Maleeva K.A.
Date: 2026-04-09
"""

import ui
import math


def gen_terms(x, max_terms=500):
    """
    Generator of series terms for cos(x).
    cos(x) = 1 - x^2/2! + x^4/4! - x^6/6! + ...
    """
    term = 1.0
    yield term
    for k in range(1, max_terms + 1):
        term *= -x * x / ((2*k - 1) * (2*k))
        yield term


def validate(func):
    """Decorator for input validation."""
    def wrapper(x, eps):
        if eps <= 0:
            raise ValueError("Epsilon must be positive")
        if eps > 0.1:
            print("Warning: Large epsilon may give inaccurate results")
        return func(x, eps)
    return wrapper


@validate
def calculate_cos(x, eps):
    """
    Calculate cos(x) using power series with given precision.
    Args:
        x: argument in radians
        eps: required precision
    Returns:
        tuple: (series_sum, terms_used, math_value)
    """
    result = 0.0
    terms_used = 0
    max_terms = 500
    for n, term in enumerate(gen_terms(x, max_terms)):
        result += term
        terms_used += 1
        if n > 0 and abs(term) < eps:
            return result, terms_used, math.cos(x)
    raise ValueError(f"Max iterations ({max_terms}) reached without convergence")


def main():
    """Main function."""
    while True:
        try:
            x = ui.read_float("Enter x (in radians): ")
            eps = ui.read_float("Enter epsilon (>0): ", min=0)
            
            result, n, math_result = calculate_cos(x, eps)
            
            ui.show_table(
                [(x, n, result, math_result, eps)],
                headers=["x", "n", "F(x)", "Math F(x)", "eps"]
            )
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        print()
        if not ui.confirm("Calculate again? (y/n): "):
            break


if __name__ == "__main__":
    main()