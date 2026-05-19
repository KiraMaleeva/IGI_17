class FigureColor:
    """Class for storing figure color"""
    
    def __init__(self, color_name: str):
        self._color = color_name
    
    @property
    def color(self) -> str:
        """Property describing the color"""
        return self._color
    
    def __str__(self) -> str:
        return self._color