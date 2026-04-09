"""
User interface module for Lab Work 3.
Provides input/output functions with validation.

Developer: Maleeva K.A.
Date: 2026-04-09
"""

import sys


def looped_input(func):
    """Decorator: repeats input until valid data is entered."""
    def wrapper(*args, **kwargs):
        while True:
            try:
                return func(*args, **kwargs)
            except ValueError:
                print("Invalid input. Try again.")
            except EOFError:
                print("\nGoodbye!")
                sys.exit(0)
    return wrapper


def bound_input(func):
    """Decorator: validates input against min/max/ranges."""
    def wrapper(*args, **kwargs):
        min_val = kwargs.pop("min", None)
        max_val = kwargs.pop("max", None)
        ranges = kwargs.pop("ranges", None)

        val = func(*args, **kwargs)

        if ranges is not None:
            for r in ranges:
                if r[0] < val < r[1]:
                    return val
            raise ValueError(f"Value must be in {ranges}")

        if min_val is not None and val < min_val:
            raise ValueError(f"Value must be at least {min_val}")

        if max_val is not None and val > max_val:
            raise ValueError(f"Value must be at most {max_val}")

        return val
    return wrapper


@looped_input
@bound_input
def read_int(prompt: str, **kwargs) -> int:
    """Read integer with validation."""
    return int(input(prompt))


@looped_input
@bound_input
def read_float(prompt: str, **kwargs) -> float:
    """Read float with validation."""
    return float(input(prompt))


@looped_input
def read_str(prompt: str, allow_empty: bool = False) -> str:
    """Read non-empty string."""
    val = input(prompt)
    if not allow_empty and val == "":
        raise ValueError("Empty string not allowed")
    return val


@looped_input
def read_float_list(prompt: str) -> list:
    """Read space-separated floats."""
    val = [float(x) for x in input(prompt).split()]
    if not val:
        raise ValueError("Empty list")
    return val


def show_table(iterable, headers=None):
    """Display data in formatted table."""

    print("-" * 66)
    
    if headers is None:
        headers = []
    
    # Print headers
    if headers:
        for h in headers:
            print(f"| {h.ljust(10)}", end=" ")
        print("|")
        for h in headers:
            print(f"|-{'-' * 10}", end="-")
        print("|")
    
    # Print rows
    for row in iterable:
        for col in row:
            if isinstance(col, float):
                print(f"| {col:.6f}".ljust(12), end=" ")
            else:
                print(f"| {str(col).ljust(10)}", end=" ")
        print("|")

    print("-" * 66)

def confirm(prompt: str) -> bool:
    """Read yes/no answer."""
    while True:
        ans = read_str(prompt).lower()
        if ans in 'y':
            return True
        if ans in 'n':
            return False
        print("Please enter y/n")


def create_seq(size: int, method: str = "generator") -> list:
    """
    Initialize sequence using generator or user input.
    """
    if method == "generator":
        return [float(i) for i in range(size)]
    else:
        print(f"Enter {size} numbers:")
        return read_float_list("> ")