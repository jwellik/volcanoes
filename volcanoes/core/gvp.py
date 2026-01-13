# File: volcanoes/core/gvp.py
import csv
import os
import warnings
from typing import List, Optional, Dict, Any
from .volcano import Volcano
from .volcano_set import VolcanoSet
from .eruption import Eruption
from .eruption_set import EruptionSet
from .gvp_downloader import GVPDownloader


class GVP:
    """Global Volcanism Program database interface."""

    def __init__(self, csv_path: Optional[str] = None, 
                 use_web_services: bool = False,
                 dataset: str = 'holocene_volcanoes',
                 cache_dir: Optional[str] = None,
                 force_refresh: bool = False):
        """Initialize the GVP database.

        Args:
            csv_path: Path to the CSV file. If None, uses the default data file or web services.
            use_web_services: If True, download data from GVP web services (lazy loading).
            dataset: Dataset to download if using web services (deprecated, use get_volcanoes/get_eruptions instead).
            cache_dir: Directory for caching downloaded data. If None, uses default cache directory.
            force_refresh: If True and using web services, force a fresh download even if cached.
        """
        self.use_web_services = use_web_services
        self.dataset = dataset  # Kept for backward compatibility
        self.downloader = None
        self.cache_dir = cache_dir
        self.force_refresh = force_refresh
        
        # Initialize downloader (used for both web services and cached data)
        self.downloader = GVPDownloader(cache_dir=cache_dir)
        
        if use_web_services:
            # Lazy loading: don't load data yet
            self.csv_path = None
            self._volcanoes = None
        else:
            # Default behavior: use most recent cached data
            if csv_path is None:
                # Use the most recent cached holocene_volcanoes file
                cache_path = self.downloader._get_cache_path('holocene_volcanoes', 'csv')
                
                if cache_path.exists():
                    # Use cached file
                    self.csv_path = str(cache_path)
                    metadata = self.downloader._load_metadata('holocene_volcanoes')
                    if metadata:
                        print(f"Using cached data (downloaded: {metadata['download_time']})")
                else:
                    # No cache exists, download it automatically
                    print("No cached data found. Downloading Holocene volcanoes from GVP web services...")
                    cache_path = self.downloader.download('holocene_volcanoes', force_refresh=False)
                    self.csv_path = str(cache_path)
            else:
                # Use the provided path
                self.csv_path = csv_path

            self._volcanoes = None
            self._load_data()

    def _load_data(self):
        """Load volcano data from CSV file (for backward compatibility)."""
        volcanoes = []

        try:
            with open(self.csv_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)

                # Check if we have the expected columns
                if reader.fieldnames:
                    print(f"CSV columns found: {reader.fieldnames}")

                for i, row in enumerate(reader):
                    try:
                        # Clean up whitespace in all fields
                        cleaned_row = {k.strip(): v.strip() if isinstance(v, str) else v
                                       for k, v in row.items() if k is not None}
                        volcanoes.append(Volcano(cleaned_row))
                    except Exception as e:
                        print(f"Error processing row {i + 1}: {e}")
                        print(f"Row data: {row}")
                        # Continue processing other rows
                        continue

            self._volcanoes = volcanoes
            print(f"Loaded {len(volcanoes)} volcanoes from {self.csv_path}")

        except FileNotFoundError:
            print(f"CSV file not found: {self.csv_path}")
            print("Please ensure the volcanoes.csv file is in the correct location.")
            print(f"Current working directory: {os.getcwd()}")
            print(f"Looking for file at: {os.path.abspath(self.csv_path)}")
            self._volcanoes = []
        except Exception as e:
            print(f"Error loading data: {e}")
            print(f"File path: {self.csv_path}")
            self._volcanoes = []

    def _load_volcanoes_from_csv(self, csv_path: str) -> List[Volcano]:
        """Load volcano data from a CSV file.
        
        Args:
            csv_path: Path to CSV file
            
        Returns:
            List of Volcano objects
        """
        volcanoes = []
        
        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                
                for i, row in enumerate(reader):
                    try:
                        # Clean up whitespace in all fields
                        cleaned_row = {k.strip(): v.strip() if isinstance(v, str) else v
                                       for k, v in row.items() if k is not None}
                        volcanoes.append(Volcano(cleaned_row))
                    except Exception as e:
                        print(f"Error processing row {i + 1}: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error loading volcanoes from {csv_path}: {e}")
            
        return volcanoes

    def _load_eruptions_from_csv(self, csv_path: str) -> List[Eruption]:
        """Load eruption data from a CSV file.
        
        Args:
            csv_path: Path to CSV file
            
        Returns:
            List of Eruption objects
        """
        eruptions = []
        
        try:
            with open(csv_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                
                for i, row in enumerate(reader):
                    try:
                        # Clean up whitespace in all fields
                        cleaned_row = {k.strip(): v.strip() if isinstance(v, str) else v
                                       for k, v in row.items() if k is not None}
                        eruptions.append(Eruption(cleaned_row))
                    except Exception as e:
                        print(f"Error processing row {i + 1}: {e}")
                        continue
                        
        except Exception as e:
            print(f"Error loading eruptions from {csv_path}: {e}")
            
        return eruptions

    def _combine_volcanoes(self, holocene_volcanoes: List[Volcano], 
                          pleistocene_volcanoes: List[Volcano]) -> List[Volcano]:
        """Combine holocene and pleistocene volcanoes, removing duplicates.
        
        Duplicates are identified by volcano number. If a volcano appears in both
        datasets, the Holocene record is kept and a warning is issued.
        
        Args:
            holocene_volcanoes: List of Holocene volcanoes
            pleistocene_volcanoes: List of Pleistocene volcanoes
            
        Returns:
            Combined list of volcanoes with duplicates removed
        """
        combined = []
        holocene_numbers = {v.volcano_number for v in holocene_volcanoes if v.volcano_number is not None}
        
        # Add all Holocene volcanoes
        combined.extend(holocene_volcanoes)
        
        # Add Pleistocene volcanoes, checking for duplicates
        duplicates = []
        for pleist in pleistocene_volcanoes:
            if pleist.volcano_number is not None:
                if pleist.volcano_number in holocene_numbers:
                    duplicates.append(pleist.volcano_number)
                else:
                    combined.append(pleist)
        
        # Issue warning if duplicates found
        if duplicates:
            warnings.warn(
                f"Found {len(duplicates)} duplicate volcano(s) in both Holocene and Pleistocene datasets "
                f"(volcano numbers: {sorted(duplicates)[:10]}{'...' if len(duplicates) > 10 else ''}). "
                f"Keeping Holocene records and discarding Pleistocene duplicates.",
                UserWarning
            )
        
        return combined

    def get_volcanoes(self, holocene: bool = True, pleistocene: bool = False) -> VolcanoSet:
        """Get volcanoes from GVP web services.
        
        Args:
            holocene: If True, include Holocene volcanoes
            pleistocene: If True, include Pleistocene volcanoes
            
        Returns:
            VolcanoSet containing the requested volcanoes
        """
        if not self.use_web_services:
            raise ValueError("get_volcanoes() requires use_web_services=True. "
                           "For local CSV files, use the 'volcanoes' property or 'filter_volcanoes()' method.")
        
        if not holocene and not pleistocene:
            return VolcanoSet([])
        
        holocene_volcs = []
        pleistocene_volcs = []
        
        if holocene:
            csv_path = self.downloader.download('holocene_volcanoes', force_refresh=self.force_refresh)
            holocene_volcs = self._load_volcanoes_from_csv(str(csv_path))
            print(f"Loaded {len(holocene_volcs)} Holocene volcanoes")
        
        if pleistocene:
            csv_path = self.downloader.download('pleistocene_volcanoes', force_refresh=self.force_refresh)
            pleistocene_volcs = self._load_volcanoes_from_csv(str(csv_path))
            print(f"Loaded {len(pleistocene_volcs)} Pleistocene volcanoes")
        
        # Combine datasets if both are requested
        if holocene and pleistocene:
            all_volcanoes = self._combine_volcanoes(holocene_volcs, pleistocene_volcs)
        elif holocene:
            all_volcanoes = holocene_volcs
        else:
            all_volcanoes = pleistocene_volcs
        
        return VolcanoSet(all_volcanoes)

    def get_eruptions(self, holocene: bool = True, pleistocene: bool = False) -> EruptionSet:
        """Get eruptions from GVP web services.
        
        Args:
            holocene: If True, include Holocene eruptions
            pleistocene: If True, include Pleistocene eruptions
            
        Returns:
            EruptionSet containing the requested eruptions
        """
        if not self.use_web_services:
            raise ValueError("get_eruptions() requires use_web_services=True.")
        
        if not holocene and not pleistocene:
            return EruptionSet([])
        
        all_eruptions = []
        
        if holocene:
            csv_path = self.downloader.download('holocene_eruptions', force_refresh=self.force_refresh)
            holocene_eruptions = self._load_eruptions_from_csv(str(csv_path))
            all_eruptions.extend(holocene_eruptions)
            print(f"Loaded {len(holocene_eruptions)} Holocene eruptions")
        
        if pleistocene:
            csv_path = self.downloader.download('pleistocene_eruptions', force_refresh=self.force_refresh)
            pleistocene_eruptions = self._load_eruptions_from_csv(str(csv_path))
            all_eruptions.extend(pleistocene_eruptions)
            print(f"Loaded {len(pleistocene_eruptions)} Pleistocene eruptions")
        
        return EruptionSet(all_eruptions)

    @property
    def volcanoes(self) -> List[Volcano]:
        """Get all volcanoes (for backward compatibility)."""
        if self.use_web_services:
            # If using web services but data hasn't been loaded yet, return empty
            # User should call get_volcanoes() instead
            if self._volcanoes is None:
                return []
        return self._volcanoes if self._volcanoes else []

    def filter_volcanoes(self,
                         country: Optional[str] = None,
                         name: Optional[str] = None,
                         id: Optional[int] = None,
                         volcano_type: Optional[str] = None,
                         geologic_epoch: Optional[str] = None,
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

        # Filter by geologic epoch
        if geologic_epoch:
            filtered = [v for v in filtered if geologic_epoch.lower() in v.geologic_epoch.lower()]

        # Filter by elevation range
        if min_elevation is not None or max_elevation is not None:
            new_filtered = []
            for v in filtered:
                elev = v.get_elevation()
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
        stats = {
            'total_volcanoes': len(self.volcanoes),
            'countries': len(self.get_countries()),
            'volcano_types': len(self.get_volcano_types()),
        }
        
        if hasattr(self, 'csv_path') and self.csv_path:
            stats['data_source'] = self.csv_path
        elif self.use_web_services:
            stats['data_source'] = 'GVP Web Services (lazy loading)'
        
        # Add cache info if using web services
        if self.use_web_services and self.downloader:
            cache_info = self.downloader.get_cache_info()
            stats['cache_info'] = cache_info
        
        return stats
    
    def export_to_csv(self, output_path: str) -> str:
        """Export current volcano data to CSV.
        
        Args:
            output_path: Path to output CSV file
            
        Returns:
            Path to the exported file
        """
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if not self.volcanoes:
                return output_path
            
            # Get fieldnames from first volcano
            fieldnames = list(self.volcanoes[0]._data.keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for volcano in self.volcanoes:
                writer.writerow(volcano._data)
        
        print(f"Exported {len(self.volcanoes)} volcanoes to {output_path}")
        return output_path
    
    def export_to_geojson(self, output_path: str) -> str:
        """Export current volcano data to GeoJSON.
        
        Args:
            output_path: Path to output GeoJSON file
            
        Returns:
            Path to the exported file
        """
        import json
        
        features = []
        for volcano in self.volcanoes:
            if volcano.lat is None or volcano.lon is None:
                continue
            
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [volcano.lon, volcano.lat]
                },
                'properties': volcano._data.copy()
            }
            features.append(feature)
        
        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, indent=2, ensure_ascii=False)
        
        print(f"Exported {len(features)} volcanoes to GeoJSON: {output_path}")
        return output_path
    
    def get_cache_info(self) -> Optional[Dict[str, Any]]:
        """Get information about cached data (if using web services).
        
        Returns:
            Cache information dictionary or None if not using web services
        """
        if self.use_web_services and self.downloader:
            return self.downloader.get_cache_info()
        return None
