"""
Laboratory Work No. 4 - Task 5
Title: NumPy Arrays and Statistical Operations
Version: 1.0
Developer: Maleeva Kira 453501
Date: 2026-05-08
"""

import numpy as np
from numpy_operations import NumPyOperations
from matrix_analyzer import MatrixAnalyzer

def get_matrix_size() -> tuple:
    """Get matrix dimensions from user with validation"""
    while True:
        try:
            n = int(input("Enter number of rows (n): "))
            m = int(input("Enter number of columns (m): "))
            if n > 0 and m > 0:
                return n, m
            print("Dimensions must be positive!")
        except ValueError:
            print("Please enter integers!")

def main():    
    # Get matrix size
    n, m = get_matrix_size()
    
    # Create matrix
    ops = NumPyOperations(n, m)
    analyzer = MatrixAnalyzer(ops.matrix)
    
    # Part a: NumPy operations
    ops.demonstrate_creation()
    ops.demonstrate_indexing()
    ops.demonstrate_universal()
    
    # Part b: Statistical operations
    print("\n Statistical Operations")
    print(f"Mean: {analyzer.mean():.2f}")
    print(f"Median: {analyzer.median():.2f}")
    print(f"Variance: {analyzer.variance():.2f}")
    print(f"Standard deviation (NumPy): {analyzer.std_numpy():.2f}")
    print(f"Standard deviation (manual): {analyzer.std_manual():.2f}")
    print(f"Correlation matrix:\n{analyzer.correlation()}")
    
    # Additional requirements
    count_above = analyzer.count_above_mean()
    std_above = analyzer.std_of_above_mean()
    print(f"\n Result")
    print(f"Elements above mean: {count_above}")
    print(f"Standard deviation of these values: {std_above}")
    
    # Repeat option
    while True:
        again = input("\nRun again? (y/n): ").strip().lower()
        if again == 'y':
            main()
            return
        elif again == 'n':
            break
        else:
            print("Enter y or n")

if __name__ == "__main__":
    main()