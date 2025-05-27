#!/usr/bin/env python3
"""
Usage Examples for the Volcanoes Package

This file demonstrates how to use the volcanoes package for various
volcano data analysis tasks.
"""

from volcanoes import GVP
import matplotlib
# matplotlib.use('TkAgg')  # or 'Qt5Agg', depending on what's available



def main():
    """Run all usage examples."""

    # Initialize the GVP database
    print("Initializing GVP database...")
    gvp = GVP()

    # Example 1: Basic database information
    print("\n" + "=" * 50)
    print("EXAMPLE 1: Database Statistics")
    print("=" * 50)

    stats = gvp.stats()
    for key, value in stats.items():
        print(f"{key}: {value}")

    # Example 2: Filter by country
    print("\n" + "=" * 50)
    print("EXAMPLE 2: Filter by Country")
    print("=" * 50)

    indonesia = gvp.filter_volcanoes(country="Indonesia")
    print(f"Found {len(indonesia)} volcanoes in Indonesia")
    indonesia.print(limit=5)  # Show first 5

    # Example 3: Filter by location and radius
    print("\n" + "=" * 50)
    print("EXAMPLE 3: Geographic Filtering")
    print("=" * 50)

    # Look for volcanoes near a specific location
    lat, lon = 40.7831, 14.7944  # Near Naples, Italy
    nearby_volcs = gvp.filter_volcanoes(latitude=lat, longitude=lon, radius_km=100.0)
    print(f"Found {len(nearby_volcs)} volcanoes within 100km of Naples")
    nearby_volcs.print()

    # Example 4: Access individual volcano details
    print("\n" + "=" * 50)
    print("EXAMPLE 4: Individual Volcano Details")
    print("=" * 50)

    if len(nearby_volcs) > 0:
        volcano = nearby_volcs[0]
        print(f"Volcano: {volcano}")
        print(f"Origin (lat, lon, elev): {volcano.origin}")
        print(f"Latitude: {volcano.lat}")
        print(f"Longitude: {volcano.lon}")
        print(f"Elevation (m): {volcano.get_elevation()}")
        print(f"Elevation (ft): {volcano.get_elevation(units='ft')}")
        print(f"Last eruption: {volcano.last_eruption_year}")
        print(f"Volcano type: {volcano.volcano_type}")
        print(f"Country: {volcano.country}")

    # Example 5: Search by name
    print("\n" + "=" * 50)
    print("EXAMPLE 5: Search by Name")
    print("=" * 50)

    etna_results = gvp.filter_volcanoes(name="Etna")
    print(f"Found {len(etna_results)} volcanoes with 'Etna' in name")
    etna_results.print()
    print()
    etna_results[0].print()
    print()
    print(etna_results[0].origin)
    print()


    # Example 6: Filter by volcano ID
    print("\n" + "=" * 50)
    print("EXAMPLE 6: Get Specific Volcano by ID")
    print("=" * 50)

    # Try to get Mount Etna (common volcano ID)
    specific_volcano = gvp.get_volcano_by_id(211060)  # Etna's typical ID
    if specific_volcano:
        print(f"Found volcano: {specific_volcano}")
        print(f"Details: {specific_volcano.geological_summary[:200]}...")
        # print(f"Geologic Epoch: {specific_volcano.geologic_epoch}")
    else:
        print("Volcano ID 211060 not found in database")

    # Example 7: Complex filtering
    print("\n" + "=" * 50)
    print("EXAMPLE 7: Complex Multi-criteria Filtering")
    print("=" * 50)

    # Find tall stratovolcanoes in Italy
    tall_stratovolcanoes = gvp.filter_volcanoes(
        volcano_type="Stratovolcano",
        min_elevation=3000,
        country="Indonesia"
    )
    print(f"Indonesian stratovolcanoes above 3000m: {len(tall_stratovolcanoes)}")
    tall_stratovolcanoes.print()

    # Example 8: Elevation-based filtering
    print("\n" + "=" * 50)
    print("EXAMPLE 8: Elevation Filtering")
    print("=" * 50)

    high_elevation = gvp.filter_volcanoes(min_elevation=3000)
    print(f"Volcanoes above 3000m: {len(high_elevation)}")
    high_elevation.print(limit=10)

    # Example 9: Volcano type analysis
    print("\n" + "=" * 50)
    print("EXAMPLE 9: Volcano Type Analysis")
    print("=" * 50)

    volcano_types = gvp.get_volcano_types()
    print(f"Available volcano types ({len(volcano_types)}):")
    for vtype in volcano_types[:10]:  # Show first 10
        count = len(gvp.filter_volcanoes(volcano_type=vtype))
        print(f"  {vtype}: {count} volcanoes")

    # Example 10: VolcanoSet operations and statistics
    print("\n" + "=" * 50)
    print("EXAMPLE 10: VolcanoSet Analysis")
    print("=" * 50)

    italy_volcs = gvp.filter_volcanoes(country="Italy")
    print(f"Italy has {len(italy_volcs)} volcanoes")

    # Get summary statistics
    summary = italy_volcs.summary_stats()
    print("\nItaly volcano statistics:")
    for key, value in summary.items():
        if isinstance(value, float) and value is not None:
            print(f"  {key}: {value:.1f}")
        else:
            print(f"  {key}: {value}")

    # Example 11: Distance-based operations
    print("\n" + "=" * 50)
    print("EXAMPLE 11: Distance Calculations")
    print("=" * 50)

    if len(italy_volcs) > 1:
        rome_lat, rome_lon = 41.9028, 12.4964  # Rome coordinates
        italy_by_distance = italy_volcs.sort_by_distance(rome_lat, rome_lon)

        print("Italian volcanoes sorted by distance from Rome:")
        for i, volcano in enumerate(italy_by_distance[:5]):  # Top 5 closest
            distance = volcano.distance_to(rome_lat, rome_lon)
            print(f"  {i + 1}. {volcano.name}: {distance:.1f} km from Rome")

    # Example 12: Working with countries
    print("\n" + "=" * 50)
    print("EXAMPLE 12: Country Analysis")
    print("=" * 50)

    countries = gvp.get_countries()
    print(f"Countries with volcanoes: {len(countries)}")

    # Show countries with most volcanoes
    country_counts = []
    for country in countries[:]:  # Check first n countries
        count = len(gvp.filter_volcanoes(country=country, geologic_epoch="Holocene"))
        country_counts.append((country, count))

    # Sort by count
    country_counts.sort(key=lambda x: x[1], reverse=True)

    print("\nTop 10 countries by Holocene volcano count:")
    for country, count in country_counts[:10]:
        print(f"  {country}: {count} volcanoes")

    # Example 13: Data exploration
    print("\n" + "=" * 50)
    print("EXAMPLE 13: Data Quality Check")
    print("=" * 50)

    all_volcanoes = gvp.volcanoes

    # Check data completeness
    with_coords = len([v for v in all_volcanoes if v.lat is not None and v.lon is not None])
    with_elevation = len([v for v in all_volcanoes if v.get_elevation() is not None])
    with_last_eruption = len([v for v in all_volcanoes if v.last_eruption_year is not None])

    print(f"Total volcanoes: {len(all_volcanoes)}")
    print(f"With coordinates: {with_coords} ({with_coords / len(all_volcanoes) * 100:.1f}%)")
    print(f"With elevation data: {with_elevation} ({with_elevation / len(all_volcanoes) * 100:.1f}%)")
    print(f"With last eruption year: {with_last_eruption} ({with_last_eruption / len(all_volcanoes) * 100:.1f}%)")

    print("\n" + "=" * 50)
    print("PLOTTING EXAMPLES (requires matplotlib)")
    print("=" * 50)
    print("To plot volcanoes, uncomment the following lines:")
    print("# italy_volcs.plot()  # Plot all Italian volcanoes")
    print("# if len(etna_results) > 0:")
    print("#     etna_results[0].plot()  # Plot Mount Etna individually")
    italy_volcs.plot()
    if len(etna_results) > 0:
        etna_results[0].plot()  # Plot Mount Etna individually

    print("\nAll examples completed successfully!")


if __name__ == "__main__":
    main()
