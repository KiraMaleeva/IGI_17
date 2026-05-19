import re
from typing import List, Tuple, Dict

class TextAnalyzer:
    """Main class for text analysis"""
    
    def __init__(self, text: str):
        self.text = text
    
    def count_sentences(self) -> Dict[str, int]:
        """
        Count total sentences and types:
        declarative (.), interrogative (?), imperative (!)
        """
        sentences = re.split(r'[.!?]+', self.text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        declarative = len(re.findall(r'[^.!?]*\.', self.text))
        interrogative = len(re.findall(r'[^.!?]*\?', self.text))
        imperative = len(re.findall(r'[^.!?]*!', self.text))
        
        return {
            'total': len(sentences),
            'declarative': declarative,
            'interrogative': interrogative,
            'imperative': imperative
        }
    
    def avg_sentence_length(self) -> float:
        """Average sentence length in characters (words only)"""
        sentences = re.split(r'[.!?]+', self.text)
        words_only_sentences = []
        
        for sent in sentences:
            words = re.findall(r'\b\w+\b', sent)
            if words:
                words_only_sentences.append(' '.join(words))
        
        if not words_only_sentences:
            return 0.0
        
        total_chars = sum(len(s) for s in words_only_sentences)
        return round(total_chars / len(words_only_sentences), 2)
    
    def avg_word_length(self) -> float:
        """Average word length in characters"""
        words = re.findall(r'\b\w+\b', self.text)
        if not words:
            return 0.0
        
        total_length = sum(len(w) for w in words)
        return round(total_length / len(words), 2)
    
    def count_smileys(self) -> int:
        """
        Count smileys matching pattern:
        start: ; or : exactly once
        then: - zero or more times
        end: one or more same brackets from ([{
        """
        pattern = r'[:;]-*[\(\)\[\]\{\}]+'
        return len(re.findall(pattern, self.text))
    
    def find_words_with_letters_f_to_y(self) -> List[str]:
        """Find all words containing letters from 'f' to 'y'"""
        pattern = r'\b\w*[fghijklmnopqrstuvwxy]\w*\b'
        words = re.findall(pattern, self.text, re.IGNORECASE)
        return list(set(words))  # unique words
    
    def extract_prices(self) -> Dict[str, List[str]]:
        """Extract prices in USD, RUR, EU"""
        patterns = {
            'USD': r'\b\d+(?:\.\d{1,2})?\s+USD\b',
            'RUR': r'\b\d+(?:\.\d{1,2})?\s+RUR\b',
            'EU': r'\b\d+(?:\.\d{1,2})?\s+EU\b'
        }
        
        prices = {}
        for currency, pattern in patterns.items():
            matches = re.findall(pattern, self.text)
            prices[currency] = matches
        
        return prices
    
    def count_short_words(self, max_length: int = 7) -> int:
        """Count words with length less than max_length"""
        words = re.findall(r'\b\w+\b', self.text)
        return len([w for w in words if len(w) < max_length])
    
    def shortest_word_ending_with_a(self) -> str:
        """Find shortest word ending with 'a'"""
        words = re.findall(r'\b\w+a\b', self.text, re.IGNORECASE)
        if not words:
            return "No word ending with 'a' found"
        return min(words, key=len)
    
    def sort_words_by_length_desc(self) -> List[str]:
        """Return all words sorted by length descending"""
        words = re.findall(r'\b\w+\b', self.text)
        return sorted(set(words), key=len, reverse=True)