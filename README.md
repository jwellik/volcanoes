# GVP VOLCANOES

Unofficial Python package for [Global Volcanism Program, Smithsonian Institution (GVP)](https://volcano.si.edu/). Downloads and caches the most recent version of the GVP Volcanoes of the World (VOTW) database available through the GVP webservices (https://volcano.si.edu/database/webservices.cfm).

## Features

- Load volcano data from CSV files or download directly from GVP web services
- Automatic caching with timestamps for downloaded data
- Export data to CSV or GeoJSON formats
- Filter and search volcanoes by various criteria
- Calculate distances between volcanoes
- Plot volcanoes on maps

## Environment Setup

Choose one of the following methods to set up the `gvp` environment:

### Option 1: Using Conda

```bash
conda env create -f environment.yml
conda activate gvp
```

### Option 2: Using uv

```bash
uv venv gvp
source gvp/bin/activate  # On Windows: gvp\Scripts\activate
```

## Installation

After setting up and activating the environment, install the package:

**If using conda:**
```bash
# Package is already installed via environment.yml
# Just verify it's working:
python -c "from volcanoes import GVP; print('Installation successful')"
```

**If using uv:**
```bash
# Install dependencies and package in editable mode
uv pip install -e .

# Or install dependencies first, then the package
uv pip install -r requirements.txt
uv pip install -e .
```

**Or using standard pip:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

**Note:** GVP data will be automatically downloaded and cached on first use. No manual download step is required.

## Quick Start

### Default Usage (Uses Cached Data)

```python
from volcanoes import GVP

# Uses most recent cached data automatically
# Downloads if no cache exists
gvp = GVP()

# Filter volcanoes
italian_volcanoes = gvp.filter_volcanoes(country="Italy")
print(f"Found {len(italian_volcanoes)} Italian volcanoes")
```

### Using GVP Web Services (Lazy Loading)

```python
from volcanoes import GVP

# Initialize with web services (lazy loading)
gvp = GVP(use_web_services=True)

# Get volcanoes (downloads/caches on demand)
volcs = gvp.get_volcanoes(holocene=True, pleistocene=False)

# Get eruptions
eruptions = gvp.get_eruptions(holocene=True, pleistocene=False)
```

### Combining Datasets

```python
from volcanoes import GVP

gvp = GVP(use_web_services=True)

# Get both Holocene and Pleistocene volcanoes
# Duplicates are automatically removed (Holocene records kept)
all_volcs = gvp.get_volcanoes(holocene=True, pleistocene=True)

# Get only Pleistocene
pleistocene_volcs = gvp.get_volcanoes(holocene=False, pleistocene=True)
```

### Exporting Data

```python
from volcanoes import GVP

gvp = GVP()

# Export to CSV
gvp.export_to_csv("volcanoes.csv")

# Export to GeoJSON
gvp.export_to_geojson("volcanoes.geojson")
```

## Data Management

### Default Behavior

By default, `GVP()` uses the **most recent cached data**. If no cache exists, it automatically downloads the default dataset (Holocene volcanoes) on first use.

### Available Datasets

- `holocene_volcanoes`: Holocene volcanoes (default)
- `holocene_eruptions`: Holocene eruptions
- `pleistocene_volcanoes`: Pleistocene volcanoes
- `pleistocene_eruptions`: Pleistocene eruptions

### Cache Management

Data downloaded from GVP web services is automatically cached with timestamps. This helps track when data was downloaded, which is important since GVP may change their data without warning.

```python
from volcanoes import GVPDownloader

downloader = GVPDownloader()

# Check cache information for all datasets
cache_info = downloader.get_cache_info()
print(cache_info)

# Force a fresh download
downloader.download('holocene_volcanoes', force_refresh=True)

# Clear cache
downloader.clear_cache('holocene_volcanoes')  # Clear specific dataset
downloader.clear_cache()  # Clear all cached data
```

### Custom Cache Directory

```python
from volcanoes import GVP

# Use a custom cache directory
gvp = GVP(cache_dir="/path/to/cache")
```

## API Reference

### GVP Class

```python
GVP(csv_path=None, use_web_services=False, dataset='holocene_volcanoes', 
    cache_dir=None, force_refresh=False)
```

- `csv_path`: Path to CSV file (optional, overrides default cached data)
- `use_web_services`: If True, enables lazy loading API (`get_volcanoes()`, `get_eruptions()`)
- `dataset`: Dataset name (deprecated, use `get_volcanoes()`/`get_eruptions()` instead)
- `cache_dir`: Custom cache directory
- `force_refresh`: Force fresh download even if cached

**Methods:**
- `get_volcanoes(holocene=True, pleistocene=False)`: Get volcanoes from web services
- `get_eruptions(holocene=True, pleistocene=False)`: Get eruptions from web services
- `filter_volcanoes(...)`: Filter volcanoes by various criteria
- `export_to_csv(output_path)`: Export to CSV
- `export_to_geojson(output_path)`: Export to GeoJSON

### GVPDownloader Class

```python
GVPDownloader(cache_dir=None, timeout=60)
```

Methods:
- `download(dataset, force_refresh=False)`: Download a dataset
- `export_to_csv(dataset, output_path=None, force_refresh=False)`: Export to CSV
- `export_to_geojson(dataset, output_path=None, force_refresh=False)`: Export to GeoJSON
- `get_cache_info(dataset=None)`: Get cache information
- `clear_cache(dataset=None)`: Clear cached data

### Volcano Class

Represents a single volcano with all its properties and methods.

**Properties:**
- `id` / `volcano_number`: Unique volcano identifier
- `name`: Volcano name
- `volcano_type`: Type of volcano (e.g., "Stratovolcano", "Shield")
- `country`: Country where the volcano is located
- `region` / `subregion`: Geographic region
- `latitude` / `lat`: Latitude coordinate
- `longitude` / `lon`: Longitude coordinate
- `elevation` / `elev`: Elevation in meters
- `last_eruption_year`: Year of last known eruption
- `geological_summary`: Detailed geological description
- `tectonic_setting`: Tectonic setting
- `geologic_epoch`: Geologic epoch (e.g., "Holocene", "Pleistocene")
- `major_rock_type`: Dominant rock type

**Methods:**
- `get_elevation(units="m")`: Get elevation in meters or feet
- `distance_to(lat, lon)`: Calculate distance to a point in kilometers
- `plot(extent_km=50.0)`: Plot volcano on a map with satellite imagery
- `simple_plot()`: Simple plot without satellite imagery
- `print()`: Print detailed volcano information

**Example:**
```python
from volcanoes import GVP

gvp = GVP()
volcano = gvp.get_volcano_by_id(211020)  # Vesuvius
print(volcano.name)  # "Vesuvius"
print(volcano.country)  # "Italy"
print(volcano.elevation)  # 1281.0 (meters)
distance = volcano.distance_to(40.8, 14.4)  # Distance in km
```

### VolcanoSet Class

A collection of volcanoes with filtering and analysis methods.

**Properties:**
- `volcanoes`: List of `Volcano` objects

**Methods:**
- `filter_by_country(country)`: Filter by country name
- `filter_by_type(volcano_type)`: Filter by volcano type
- `filter_by_elevation_range(min_elev, max_elev)`: Filter by elevation range
- `sort_by_distance(lat, lon)`: Sort volcanoes by distance from a point
- `within_radius(lat, lon, radius_km)`: Get volcanoes within a radius
- `get_lats()` / `get_lons()` / `get_elevs()`: Get lists of coordinates/elevations
- `print(limit=None)`: Print information about volcanoes
- `plot()`: Plot all volcanoes on a map
- `simple_plot()`: Simple plot without satellite imagery
- `summary_stats()`: Get summary statistics

**Example:**
```python
from volcanoes import GVP

gvp = GVP()
italian_volcs = gvp.filter_volcanoes(country="Italy")
print(f"Found {len(italian_volcs)} Italian volcanoes")

# Filter and sort by distance
nearby = italian_volcs.within_radius(40.8, 14.4, radius_km=100)
sorted_volcs = nearby.sort_by_distance(40.8, 14.4)
sorted_volcs.print(limit=5)
```

### Eruption Class

**Note:** This is currently a stub class with basic functionality. Full implementation is planned for future development.

Represents a single volcanic eruption. Currently provides basic data access with flexible field handling for unknown CSV fields.

**Properties:**
- `volcano_number` / `id`: Volcano identifier associated with the eruption
- `eruption_number`: Unique eruption identifier (if available)

**Methods:**
- `get_field(field_name, default=None)`: Get any field value by name
- Dictionary-like access: `eruption['FieldName']` to access data fields

**Example:**
```python
from volcanoes import GVP

gvp = GVP(use_web_services=True)
eruptions = gvp.get_eruptions(holocene=True)

for eruption in eruptions[:5]:
    print(f"Volcano #{eruption.volcano_number}")
    # Access unknown fields using get_field() or dictionary access
    year = eruption.get_field('Year')
    vei = eruption['VEI']
```

### EruptionSet Class

**Note:** This is currently a stub class with basic functionality. Full implementation is planned for future development.

A collection of eruptions with basic filtering methods.

**Properties:**
- `eruptions`: List of `Eruption` objects

**Methods:**
- `filter_by_volcano_number(volcano_number)`: Filter eruptions by volcano number
- `get_volcano_numbers()`: Get list of unique volcano numbers
- `print(limit=None)`: Print information about eruptions
- `summary_stats()`: Get summary statistics

**Example:**
```python
from volcanoes import GVP

gvp = GVP(use_web_services=True)
eruptions = gvp.get_eruptions(holocene=True)

# Filter eruptions for a specific volcano
vesuvius_eruptions = eruptions.filter_by_volcano_number(211020)
print(f"Found {len(vesuvius_eruptions)} eruptions for Vesuvius")
```

## Notes

- **No bundled data**: The package no longer includes bundled CSV files. All data is downloaded and cached on first use.
- **Default behavior**: `GVP()` uses the most recent cached data. If no cache exists, it automatically downloads the default dataset.
- **Data versioning**: The GVP web services sometimes change data without warning. The caching system with timestamps helps track when data was downloaded.
- **XML syntax fix**: A known issue with GVP web services XML syntax is automatically handled (replacing `(< ` with `(&lt; `).
- **Cache location**: By default, cached data is stored in `~/.volcanoes_cache/`.

## Examples

See `examples/new_api_example.py` and `examples/gvp_web_services_example.py` for detailed examples.

## Development Status

This code is in active development.