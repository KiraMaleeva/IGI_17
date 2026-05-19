from collections import Counter
from typing import List, Any

class StatisticsCalculator:
    """Helper class for statistical calculations"""
    
    @staticmethod
    def mode(data: List[Any]) -> List[Any]:
        """Calculate mode (most frequent values)"""
        if not data:
            return []
        counter = Counter(data)
        max_freq = max(counter.values())
        return [item for item, freq in counter.items() if freq == max_freq]
    
    @staticmethod
    def get_word_frequencies(text: str) -> dict:
        """Get word frequency dictionary"""
        import re
        words = re.findall(r'\b\w+\b', text.lower())
        return dict(Counter(words))