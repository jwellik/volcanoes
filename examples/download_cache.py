"""
Example: Download and Cache GVP Data

This example demonstrates:
- Downloading data from GVP web services
- Automatic caching in project directory
- Using get_volcanoes() and get_eruptions() methods
- Filtering and exporting data
"""

from volcanoes import GVP


def example_basic_usage():
    """Basic example: Using the new API."""
    print("=" * 60)
    print("Example 1: Basic usage with new API")
    print("=" * 60)
    
    # Initialize with web services (lazy loading - no data downloaded yet)
    gvp = GVP(use_web_services=True)
    
    # Get Holocene volcanoes (downloads if not cached, uses cache if available)
    volcs = gvp.get_volcanoes(holocene=True, pleistocene=False)
    print(f"\nHolocene volcanoes: {len(volcs)}")
    volcs.print(limit=5)
    
    # Get eruptions
    eruptions = gvp.get_eruptions(holocene=True, pleistocene=False)
    print(f"\nHolocene eruptions: {len(eruptions)}")
    eruptions.print(limit=5)


def example_combining_datasets():
    """Example: Combining Holocene and Pleistocene data."""
    print("\n" + "=" * 60)
    print("Example 2: Combining Holocene and Pleistocene")
    print("=" * 60)
    
    gvp = GVP(use_web_services=True)
    
    # Get both Holocene and Pleistocene volcanoes
    # Duplicates (by volcano number) will be removed, keeping Holocene records
    all_volcs = gvp.get_volcanoes(holocene=True, pleistocene=True)
    print(f"\nAll volcanoes (Holocene + Pleistocene): {len(all_volcs)}")
    
    # Get only Pleistocene
    pleistocene_volcs = gvp.get_volcanoes(holocene=False, pleistocene=True)
    print(f"\nPleistocene only: {len(pleistocene_volcs)}")


def example_cache_behavior():
    """Example: Demonstrating cache behavior."""
    print("\n" + "=" * 60)
    print("Example 3: Cache behavior")
    print("=" * 60)
    
    gvp = GVP(use_web_services=True)
    
    # First call - will download if not cached
    print("\nFirst call (will use cache if available, download if not):")
    volcs1 = gvp.get_volcanoes(holocene=True)
    
    # Second call - will use cached data
    print("\nSecond call (will use cached data):")
    volcs2 = gvp.get_volcanoes(holocene=True)
    
    # Check cache info
    cache_info = gvp.get_cache_info()
    print("\nCache information:")
    for dataset, info in cache_info.items():
        if info.get('cached'):
            print(f"  {dataset}: cached (downloaded {info['download_time']})")
        else:
            print(f"  {dataset}: not cached")


def example_backward_compatibility():
    """Example: Backward compatibility with old API."""
    print("\n" + "=" * 60)
    print("Example 4: Backward compatibility")
    print("=" * 60)
    
    # Old way still works - loads from local CSV immediately
    gvp_old = GVP(use_web_services=False)
    print(f"\nOld API: {len(gvp_old.volcanoes)} volcanoes loaded from local CSV")
    
    # Can still use filter_volcanoes
    italian = gvp_old.filter_volcanoes(country="Italy")
    print(f"Italian volcanoes: {len(italian)}")


def example_export_filtered_data():
    """Example: Filter and export data to CSV and GeoJSON."""
    print("\n" + "=" * 60)
    print("Example 5: Filter and export Indonesia volcanoes")
    print("=" * 60)
    
    gvp = GVP(use_web_services=True)
    
    # Get Holocene volcanoes
    volcanoes = gvp.get_volcanoes(holocene=True)
    
    # Filter to Indonesia
    indonesia_volcanoes = volcanoes.filter_by_country("Indonesia")
    print(f"\nFound {len(indonesia_volcanoes)} volcanoes in Indonesia")
    indonesia_volcanoes.print(limit=5)
    
    # Export to CSV
    csv_path = indonesia_volcanoes.export_to_csv("indonesia_volcanoes.csv")
    print(f"\nExported to CSV: {csv_path}")
    
    # Export to GeoJSON
    geojson_path = indonesia_volcanoes.export_to_geojson("indonesia_volcanoes.geojson")
    print(f"Exported to GeoJSON: {geojson_path}")


if __name__ == "__main__":
    try:
        example_basic_usage()
        example_combining_datasets()
        example_cache_behavior()
        example_backward_compatibility()
        example_export_filtered_data()
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
