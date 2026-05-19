"""
NumPy operations for Task 5
Developer: Maleeva Kira 453501
"""

import numpy as np

class NumPyOperations:
    """Demonstrates NumPy array operations"""
    
    def __init__(self, n: int, m: int):
        """Create random integer matrix"""
        self.matrix = np.random.randint(1, 100, size=(n, m))
    
    def demonstrate_creation(self):
        """1. array() and 2. array creation functions"""
        print("\n Array Creation")
        print(f"array(): {np.array([1, 2, 3])}")
        print(f"zeros(): {np.zeros((2, 3))}")
        print(f"ones(): {np.ones((2, 3))}")
        print(f"eye(): {np.eye(3)}")
        print(f"Random matrix {self.matrix.shape}:\n{self.matrix}")
    
    def demonstrate_indexing(self):
        """3. Indexing and slicing"""
        print("\n Indexing and Slicing")
        print(f"Element [0,0]: {self.matrix[0, 0]}")
        print(f"First row: {self.matrix[0, :]}")
        print(f"First column: {self.matrix[:, 0]}")
        print(f"Submatrix [:2, :2]:\n{self.matrix[:2, :2]}")
    
    def demonstrate_universal(self):
        """4. Universal functions"""
        print("\n Universal Functions")
        print(f"Matrix + 10:\n{self.matrix + 10}")
        print(f"Matrix * 2:\n{self.matrix * 2}")
        print(f"sin(x):\n{np.sin(self.matrix / 10)}")
        print(f"sqrt(x):\n{np.sqrt(self.matrix)}")