import numpy as np
import math

class MatrixAnalyzer:
    """Statistical analysis of matrix"""
    
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix
        self.data = matrix.flatten()
    
    def mean(self) -> float:
        """1. mean() function"""
        return np.mean(self.data)
    
    def median(self) -> float:
        """2. median() function"""
        return np.median(self.data)
    
    def variance(self) -> float:
        """3. var() function"""
        return np.var(self.data)
    
    def std_numpy(self) -> float:
        """4. std() function (NumPy)"""
        return np.std(self.data)
    
    def std_manual(self) -> float:
        """5. std() calculated manually using formula"""
        mean_val = self.mean()
        squared_diff = sum((x - mean_val) ** 2 for x in self.data)
        return math.sqrt(squared_diff / len(self.data))
    
    def correlation(self) -> np.ndarray:
        """corrcoef() function"""
        return np.corrcoef(self.matrix)
    
    def count_above_mean(self) -> int:
        """Count elements greater than mean"""
        mean_val = self.mean()
        return len(self.data[self.data > mean_val])
    
    def std_of_above_mean(self) -> float:
        """Standard deviation of elements above mean"""
        mean_val = self.mean()
        above_mean = self.data[self.data > mean_val]
        if len(above_mean) > 1:
            return round(np.std(above_mean), 2)
        return 0.0