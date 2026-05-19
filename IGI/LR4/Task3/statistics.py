from typing import List, Union, Dict
from collections import Counter
import math


class SequenceStatistics:
    """Calculate statistical parameters of a sequence."""
    
    @staticmethod
    def mean(data: List[Union[int, float]]) -> float:
        """Arithmetic mean."""
        return sum(data) / len(data) if data else 0.0
    
    @staticmethod
    def median(data: List[Union[int, float]]) -> float:
        """Median."""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2
        return sorted_data[mid]
    
    @staticmethod
    def mode(data: List[Union[int, float]]) -> list:
        """Mode (most frequent values)."""
        if not data:
            return []
        counter = Counter(data)
        max_freq = max(counter.values())
        if max_freq == 1:
            return []
        return [v for v, f in counter.items() if f == max_freq]
    
    @staticmethod
    def variance(data: List[Union[int, float]]) -> float:
        """Sample variance."""
        if len(data) < 2:
            return 0.0
        mean_val = SequenceStatistics.mean(data)
        squared_diffs = [(x - mean_val) ** 2 for x in data]
        return sum(squared_diffs) / (len(data) - 1)
    
    @staticmethod
    def std_deviation(data: List[Union[int, float]]) -> float:
        """Standard deviation (СКО)."""
        return math.sqrt(SequenceStatistics.variance(data))
    
    @staticmethod
    def get_all(data: List[Union[int, float]]) -> Dict[str, Union[float, list]]:
        """Get all statistics at once."""
        return {
            'mean': round(SequenceStatistics.mean(data), 4),
            'median': round(SequenceStatistics.median(data), 4),
            'mode': SequenceStatistics.mode(data),
            'variance': round(SequenceStatistics.variance(data), 4),
            'std': round(SequenceStatistics.std_deviation(data), 4),
            'min': min(data),
            'max': max(data),
            'count': len(data)
        }