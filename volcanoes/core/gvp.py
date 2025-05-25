# File: volcanoes/core/gvp.py
import csv
import os
from typing import List, Optional, Dict, Any
from .volcano import Volcano
from .volcano_set import VolcanoSet


class GVP:
    """Global Volcanism Program database interface."""

    def __init__(self, csv_path: Optional[str] = None):
        """Initialize the GVP database.

        Args:
            csv_path: Path to the CSV file. If None, uses the default data file.
        """

        if csv_path is None:
            # Try to use importlib.resources first
            try:
                from importlib import resources
                with resources.path('volcanoes.data', 'volcanoes.csv') as data_path:
                    self.csv_path = str(data_path)
            except ImportError:
                # Fallback for older Python versions
                package_dir = os.path.dirname(os.path.dirname(__file__))
                self.csv_path = os.path.join(package_dir, 'data', 'volcanoes.csv')
            except (ModuleNotFoundError, FileNotFoundError):
                # Fallback if the data module doesn't exist
                package_dir = os.path.dirname(os.path.dirname(__file__))
                self.csv_path = os.path.join(package_dir, 'data', 'volcanoes.csv')
        else:
            # Use the provided path
            self.csv_path = csv_path

        self._volcanoes = None
        self._load_data()

    def _load_data(self):
        """Load volcano data from CSV file."""
        volcanoes = []

        try:
            with open(self.csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Clean up whitespace in all fields
                    cleaned_row = {k.strip(): v.strip() if isinstance(v, str) else v
                                   for k, v in row.items()}
                    volcanoes.append(Volcano(cleaned_row))

            self._volcanoes = volcanoes
            print(f"Loaded {len(volcanoes)} volcanoes from {self.csv_path}")

        except FileNotFoundError:
            print(f"CSV file not found: {self.csv_path}")
            print("Please ensure the volcanoes.csv file is in the correct location.")
            self._volcanoes = []
        except Exception as e:
            print(f"Error loading data: {e}")
            self._volcanoes = []

    @property
    def volcanoes(self) -> List[Volcano]:
        """Get all volcanoes."""
        return self._volcanoes if self._volcanoes else []

    def filter_volcanoes(self,
                         country: Optional[str] = None,
                         name: Optional[str] = None,
                         id: Optional[int] = None,
                         volcano_type: Optional[str] = None,
                         latitude: Optional[float] = None,
                         longitude: Optional[float] = None,
                         radius_km: Optional[float] = None,
                         min_elevation: Optional[float] = None,
                         max_elevation: Optional[float] = None) -> VolcanoSet:
        """Filter volcanoes based on various criteria.

        Args:
            country: Filter by country name
            name: Filter by volcano name (partial match)
            id: Filter by volcano number/ID
            volcano_type: Filter by volcano type (partial match)
            latitude: Latitude for distance-based filtering
            longitude: Longitude for distance-based filtering
            radius_km: Radius in km for distance-based filtering
            min_elevation: Minimum elevation filter
            max_elevation: Maximum elevation filter

        Returns:
            VolcanoSet containing matching volcanoes
        """
        filtered = self.volcanoes.copy()

        # Filter by country
        if country:
            filtered = [v for v in filtered if country.lower() in v.country.lower()]

        # Filter by name
        if name:
            filtered = [v for v in filtered if name.lower() in v.name.lower()]

        # Filter by ID
        if id is not None:
            filtered = [v for v in filtered if v.id == id]

        # Filter by volcano type
        if volcano_type:
            filtered = [v for v in filtered if volcano_type.lower() in v.volcano_type.lower()]

        # Filter by elevation range
        if min_elevation is not None or max_elevation is not None:
            new_filtered = []
            for v in filtered:
                elev = v.elevation()
                if elev is not None:
                    if min_elevation is not None and elev < min_elevation:
                        continue
                    if max_elevation is not None and elev > max_elevation:
                        continue
                    new_filtered.append(v)
            filtered = new_filtered

        # Create VolcanoSet
        volcano_set = VolcanoSet(filtered)

        # Apply distance-based filtering and sorting
        if latitude is not None and longitude is not None:
            if radius_km is not None:
                volcano_set = volcano_set.within_radius(latitude, longitude, radius_km)
            volcano_set = volcano_set.sort_by_distance(latitude, longitude)

        return volcano_set

    def get_volcano_by_id(self, volcano_id: int) -> Optional[Volcano]:
        """Get a single volcano by its ID."""
        result = self.filter_volcanoes(id=volcano_id)
        return result[0] if len(result) > 0 else None

    def get_countries(self) -> List[str]:
        """Get a list of all countries with volcanoes."""
        countries = list(set(v.country for v in self.volcanoes if v.country))
        return sorted(countries)

    def get_volcano_types(self) -> List[str]:
        """Get a list of all volcano types."""
        types = list(set(v.volcano_type for v in self.volcanoes if v.volcano_type))
        return sorted(types)

    def stats(self) -> Dict[str, Any]:
        """Get database statistics."""
        return {
            'total_volcanoes': len(self.volcanoes),
            'countries': len(self.get_countries()),
            'volcano_types': len(self.get_volcano_types()),
            'data_source': self.csv_path
        }