"""
GVP Web Services Downloader and Cache Manager

This module handles downloading data from GVP web services, caching with timestamps,
and exporting to various formats (CSV, GeoJSON).
"""
import os
import csv
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any
from urllib.parse import urlparse


class GVPDownloader:
    """Download and cache GVP web services data."""
    
    # GVP Web Services base URL
    BASE_URL = "https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows"
    
    # Available datasets
    DATASETS = {
        'holocene_volcanoes': 'GVP-VOTW:Smithsonian_VOTW_Holocene_Volcanoes',
        'holocene_eruptions': 'GVP-VOTW:Smithsonian_VOTW_Holocene_Eruptions',
        'pleistocene_volcanoes': 'GVP-VOTW:Smithsonian_VOTW_Pleistocene_Volcanoes',
        'pleistocene_eruptions': 'GVP-VOTW:Smithsonian_VOTW_Pleistocene_Eruptions',
    }
    
    def __init__(self, cache_dir: Optional[str] = None, timeout: int = 60):
        """Initialize the GVP downloader.
        
        Args:
            cache_dir: Directory to store cached files. If None, uses a default cache directory.
            timeout: Request timeout in seconds.
        """
        if cache_dir is None:
            # Use a cache directory in the current working directory (project directory)
            cache_dir = os.path.join(os.getcwd(), ".volcanoes_cache")
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.timeout = timeout
        
    def _get_cache_path(self, dataset: str, format: str = 'csv') -> Path:
        """Get the cache file path for a dataset.
        
        Args:
            dataset: Dataset name (e.g., 'holocene_volcanoes')
            format: File format ('csv' or 'geojson')
            
        Returns:
            Path to the cache file
        """
        return self.cache_dir / f"{dataset}.{format}"
    
    def _get_metadata_path(self, dataset: str) -> Path:
        """Get the metadata file path for a dataset.
        
        Args:
            dataset: Dataset name
            
        Returns:
            Path to the metadata file
        """
        return self.cache_dir / f"{dataset}.meta.json"
    
    def _get_download_url(self, dataset: str, output_format: str = 'csv') -> str:
        """Get the download URL for a dataset.
        
        Args:
            dataset: Dataset name (key from DATASETS)
            output_format: Output format ('csv' or 'geojson')
            
        Returns:
            Download URL
        """
        if dataset not in self.DATASETS:
            raise ValueError(f"Unknown dataset: {dataset}. Available: {list(self.DATASETS.keys())}")
        
        type_name = self.DATASETS[dataset]
        
        # Build WFS request URL
        params = {
            'service': 'WFS',
            'version': '1.0.0',
            'request': 'GetFeature',
            'typeName': type_name,
            'outputFormat': output_format if output_format == 'geojson' else 'csv'
        }
        
        # Build query string
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        url = f"{self.BASE_URL}?{query_string}"
        
        return url
    
    def _download_data(self, url: str) -> bytes:
        """Download data from a URL.
        
        Args:
            url: URL to download from
            
        Returns:
            Downloaded data as bytes
        """
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Handle XML syntax issue: replace "(< " with "(&lt; "
            # This fixes a known issue with GVP web services
            content = response.content
            if b'(< ' in content:
                content = content.replace(b'(< ', b'(&lt; ')
            
            return content
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to download data from {url}: {e}")
    
    def _save_metadata(self, dataset: str, download_time: datetime, file_path: Path):
        """Save metadata about a cached file.
        
        Args:
            dataset: Dataset name
            download_time: When the data was downloaded
            file_path: Path to the cached file
        """
        metadata = {
            'dataset': dataset,
            'download_time': download_time.isoformat(),
            'download_timestamp': download_time.timestamp(),
            'file_path': str(file_path),
            'file_size': file_path.stat().st_size if file_path.exists() else 0,
        }
        
        metadata_path = self._get_metadata_path(dataset)
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def _load_metadata(self, dataset: str) -> Optional[Dict[str, Any]]:
        """Load metadata for a cached dataset.
        
        Args:
            dataset: Dataset name
            
        Returns:
            Metadata dictionary or None if not found
        """
        metadata_path = self._get_metadata_path(dataset)
        if not metadata_path.exists():
            return None
        
        try:
            with open(metadata_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None
    
    def download(self, dataset: str, force_refresh: bool = False) -> Path:
        """Download a dataset from GVP web services.
        
        Args:
            dataset: Dataset name (e.g., 'holocene_volcanoes')
            force_refresh: If True, download even if cached data exists
            
        Returns:
            Path to the downloaded/cached CSV file
        """
        if dataset not in self.DATASETS:
            raise ValueError(f"Unknown dataset: {dataset}. Available: {list(self.DATASETS.keys())}")
        
        cache_path = self._get_cache_path(dataset, 'csv')
        
        # Check if we have cached data and if we should use it
        if not force_refresh and cache_path.exists():
            metadata = self._load_metadata(dataset)
            if metadata:
                print(f"Using cached data for {dataset} (downloaded: {metadata['download_time']})")
                return cache_path
        
        # Download fresh data
        print(f"Downloading {dataset} from GVP web services...")
        url = self._get_download_url(dataset, 'csv')
        data = self._download_data(url)
        
        # Save to cache
        cache_path.write_bytes(data)
        
        # Save metadata
        download_time = datetime.now()
        self._save_metadata(dataset, download_time, cache_path)
        
        print(f"Downloaded and cached {dataset} ({len(data)} bytes)")
        return cache_path
    
    def export_to_csv(self, dataset: str, output_path: Optional[str] = None, 
                     force_refresh: bool = False) -> Path:
        """Download and export a dataset to CSV.
        
        Args:
            dataset: Dataset name
            output_path: Output file path. If None, uses cache path.
            force_refresh: If True, download fresh data even if cached
            
        Returns:
            Path to the exported CSV file
        """
        cache_path = self.download(dataset, force_refresh=force_refresh)
        
        if output_path:
            output_path = Path(output_path)
            # Copy cached file to output path
            import shutil
            shutil.copy2(cache_path, output_path)
            return output_path
        
        return cache_path
    
    def export_to_geojson(self, dataset: str, output_path: Optional[str] = None,
                         force_refresh: bool = False) -> Path:
        """Download and export a dataset to GeoJSON.
        
        Args:
            dataset: Dataset name
            output_path: Output file path. If None, generates a name based on dataset.
            force_refresh: If True, download fresh data even if cached
            
        Returns:
            Path to the exported GeoJSON file
        """
        if output_path is None:
            output_path = self.cache_dir / f"{dataset}.geojson"
        else:
            output_path = Path(output_path)
        
        # First, download as CSV
        csv_path = self.download(dataset, force_refresh=force_refresh)
        
        # Convert CSV to GeoJSON
        self._csv_to_geojson(csv_path, output_path)
        
        return output_path
    
    def _csv_to_geojson(self, csv_path: Path, geojson_path: Path):
        """Convert CSV file to GeoJSON format.
        
        Args:
            csv_path: Path to input CSV file
            geojson_path: Path to output GeoJSON file
        """
        features = []
        
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Extract coordinates
                try:
                    lat = float(row.get('Latitude', row.get('latitude', 0)))
                    lon = float(row.get('Longitude', row.get('longitude', 0)))
                except (ValueError, KeyError):
                    # Skip rows without valid coordinates
                    continue
                
                # Create GeoJSON feature
                feature = {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [lon, lat]
                    },
                    'properties': {}
                }
                
                # Add all other fields as properties
                for key, value in row.items():
                    if key.lower() not in ['latitude', 'longitude', 'lat', 'lon']:
                        # Try to convert numeric values
                        try:
                            if '.' in str(value):
                                feature['properties'][key] = float(value)
                            else:
                                feature['properties'][key] = int(value)
                        except (ValueError, TypeError):
                            feature['properties'][key] = value
                
                features.append(feature)
        
        # Create GeoJSON FeatureCollection
        geojson = {
            'type': 'FeatureCollection',
            'features': features
        }
        
        # Write to file
        with open(geojson_path, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, indent=2, ensure_ascii=False)
        
        print(f"Exported {len(features)} features to GeoJSON: {geojson_path}")
    
    def get_cache_info(self, dataset: Optional[str] = None) -> Dict[str, Any]:
        """Get information about cached datasets.
        
        Args:
            dataset: Specific dataset name, or None for all datasets
            
        Returns:
            Dictionary with cache information
        """
        if dataset:
            datasets = [dataset]
        else:
            datasets = list(self.DATASETS.keys())
        
        info = {}
        for ds in datasets:
            metadata = self._load_metadata(ds)
            cache_path = self._get_cache_path(ds, 'csv')
            
            if cache_path.exists() and metadata:
                info[ds] = {
                    'cached': True,
                    'download_time': metadata['download_time'],
                    'file_size': metadata['file_size'],
                    'file_path': str(cache_path),
                }
            else:
                info[ds] = {
                    'cached': False,
                    'file_path': str(cache_path),
                }
        
        return info
    
    def clear_cache(self, dataset: Optional[str] = None):
        """Clear cached data.
        
        Args:
            dataset: Specific dataset to clear, or None to clear all
        """
        if dataset:
            datasets = [dataset]
        else:
            datasets = list(self.DATASETS.keys())
        
        for ds in datasets:
            cache_path = self._get_cache_path(ds, 'csv')
            metadata_path = self._get_metadata_path(ds)
            
            if cache_path.exists():
                cache_path.unlink()
                print(f"Removed cache for {ds}")
            
            if metadata_path.exists():
                metadata_path.unlink()
