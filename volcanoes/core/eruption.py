"""
Eruption class for representing volcanic eruptions.
"""
from typing import Optional, Dict, Any


class Eruption:
    """Represents a single volcanic eruption with all its properties."""

    def __init__(self, data: Dict[str, Any]):
        """Initialize an Eruption object from a dictionary of data."""
        self._data = data
        self._process_data()

    def _process_data(self):
        """Process and clean the raw data."""
        # Convert numeric fields - we'll discover these as we work with the data
        # Common fields that might be numeric
        numeric_fields = ['VolcanoNumber', 'EruptionNumber', 'Year', 'StartYear', 
                         'EndYear', 'Latitude', 'Longitude', 'VEI']
        for field in numeric_fields:
            if field in self._data and self._data[field] != '':
                try:
                    if field in ['VolcanoNumber', 'EruptionNumber']:
                        self._data[field] = int(self._data[field])
                    else:
                        self._data[field] = float(self._data[field])
                except (ValueError, TypeError):
                    self._data[field] = None

    @property
    def volcano_number(self) -> Optional[int]:
        """Get the volcano number (unique identifier for the volcano)."""
        return self._data.get('VolcanoNumber')

    @property
    def id(self) -> Optional[int]:
        """Alias for volcano_number."""
        return self.volcano_number

    @property
    def eruption_number(self) -> Optional[int]:
        """Get the eruption number if available."""
        return self._data.get('EruptionNumber')

    def get_field(self, field_name: str, default=None):
        """Get a field value by name (for unknown fields)."""
        return self._data.get(field_name, default)

    def __getitem__(self, key: str):
        """Allow dictionary-like access to data."""
        return self._data.get(key)

    def __str__(self) -> str:
        """String representation of the eruption."""
        volcano_num = self.volcano_number if self.volcano_number else "Unknown"
        return f"Eruption (Volcano #{volcano_num})"

    def __repr__(self) -> str:
        """Detailed representation of the eruption."""
        volcano_num = self.volcano_number if self.volcano_number else "Unknown"
        return f"Eruption(volcano_number={volcano_num})"
