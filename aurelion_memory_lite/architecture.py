"""
AURELION Memory-Lite Architecture Implementation
Implements the 5-floor library system.
"""

class Architecture:
    """Manages the 5-floor knowledge architecture."""
    
    FLOORS = {
        1: "Foundation",
        2: "Systems", 
        3: "Networks",
        4: "Action",
        5: "Vision"
    }
    
    def __init__(self):
        self.floors = self.FLOORS
    
    def get_floor(self, number):
        """Get floor name by number."""
        return self.floors.get(number, "Unknown")
    
    def get_all_floors(self):
        """Get all floors."""
        return self.floors
