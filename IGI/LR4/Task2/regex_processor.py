import re

class RegexProcessor:
    """Specialized class for regex operations"""
    
    @staticmethod
    def find_valid_prices(text: str) -> list:
        """
        Extract valid prices with currencies
        Valid examples: 23.78 USD, 100 RUR, 50.5 EU
        Invalid: 22 UDD, 0.002 USD
        """
        pattern = r'\b\d+(?:\.\d{1,2})?\s+(?:USD|RUR|EU)\b'
        return re.findall(pattern, text)
    
    @staticmethod
    def validate_smiley(smiley: str) -> bool:
        """Validate if a string is a correct smiley"""
        pattern = r'^[:;]-*[\(\)\[\]\{\}]+$'
        return bool(re.match(pattern, smiley))