class Student:
    """Class representing a student"""
    
    # Static attribute (class-level)
    school_name = "School No. 17"
    
    # Dynamic attributes are instance-level
    
    def __init__(self, last_name: str, birth_day: int, birth_month: int, birth_year: int):
        self._last_name = last_name
        self._birth_day = birth_day
        self._birth_month = birth_month
        self._birth_year = birth_year
    
    # Properties (getters/setters)
    @property
    def last_name(self):
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        if not value.strip():
            raise ValueError("Last name cannot be empty")
        self._last_name = value
    
    @property
    def birth_month(self):
        return self._birth_month
    
    @birth_month.setter
    def birth_month(self, value):
        if not 1 <= value <= 12:
            raise ValueError("Month must be between 1 and 12")
        self._birth_month = value
    
    # Magic method
    def __str__(self):
        return f"{self._last_name}: {self._birth_day:02d}.{self._birth_month:02d}.{self._birth_year}"
    
    def __repr__(self):
        return f"Student('{self._last_name}', {self._birth_day}, {self._birth_month}, {self._birth_year})"