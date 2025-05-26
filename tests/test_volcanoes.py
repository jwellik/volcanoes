# File: examples/usage_examples.py
"""
Examples of how to use the volcanoes package
"""

from volcanoes import GVP

# Initialize the GVP database
print("Initializing GVP database...")
gvp = GVP()

# Example 1: Filter by country
print("\n=== Example 1: Filter by Country ===")
indonesia = gvp.filter_volcanoes(country="Indonesia")
print(f"Found {len(indonesia)} volcanoes in Indonesia")
indonesia.print(limit=5)  # Show first 5

# Example 2: Filter by location and radius
print("\n=== Example 2: Filter by Location and Radius ===")
volcs = gvp.filter_volcanoes(latitude=34.456, longitude=-178.077, radius_km=100.0)
print(f"Found {len(volcs)} volcanoes within 100km of (34.456, -178.077)")
volcs.print()

# Example 3: Access individual volcano
print("\n=== Example 3: Individual Volcano Access ===")
if len(volcs) > 0:
    volc0 = volcs[0]
    print(f"First volcano: {volc0}")
    print(f"Origin: {volc0.origin}")
    print(f"Latitude: {volc0.lat}")
    print(f"Elevation (m): {volc0.get_elevation()}")
    print(f"Elevation (ft): {volc0.get_elevation(units='ft')}")
    print(f"Last eruption: {volc0.last_eruption_year}")

# Example 4: Filter by name
print("\n=== Example 4: Filter by Name ===")
etna = gvp.filter_volcanoes(name="Etna")
print(f"Found {len(etna)} volcanoes with 'Etna' in name")
etna.print()

# Example 5: Filter by volcano ID
print("\n=== Example 5: Filter by Volcano ID ===")
volcano_211060 = gvp.filter_volcanoes(id=211060)  # Etna's ID
print(f"Volcano with ID 211060:")
volcano_211060.print()

# Example 6: Database statistics
print("\n=== Example 6: Database Statistics ===")
stats = gvp.stats()
for key, value in stats.items():
    print(f"{key}: {value}")

# Example 7: Get available countries and types
print("\n=== Example 7: Available Data ===")
countries = gvp.get_countries()
print(f"Countries with volcanoes: {countries[:10]}...")  # Show first 10

volcano_types = gvp.get_volcano_types()
print(f"Volcano types: {volcano_types}")

# Example 8: Complex filtering
print("\n=== Example 8: Complex Filtering ===")
tall_stratovolcanoes = gvp.filter_volcanoes(
    volcano_type="Stratovolcano",
    min_elevation=2000,
    country="Italy"
)
print(f"Italian stratovolcanoes above 2000m: {len(tall_stratovolcanoes)}")
tall_stratovolcanoes.print()

# Example 9: Volcano set operations
print("\n=== Example 9: VolcanoSet Operations ===")
italy_volcs = gvp.filter_volcanoes(country="Italy")
print(f"Italy has {len(italy_volcs)} volcanoes")

# Get summary statistics
summary = italy_volcs.summary_stats()
print("Italy volcano statistics:")
for key, value in summary.items():
    if isinstance(value, float):
        print(f"  {key}: {value:.1f}")
    else:
        print(f"  {key}: {value}")

# Example 10: Plotting (requires matplotlib)
print("\n=== Example 10: Plotting ===")
print("Plotting requires matplotlib. If installed, uncomment the lines below:")
italy_volcs.plot()  # Plot all Italian volcanoes
if len(etna) > 0:
    etna[0].plot()  # Plot Mount Etna individually

print("\nAll examples completed!")

# Additional examples for testing different scenarios

print("\n=== Additional Tests ===")

# Test unnamed volcano handling
unnamed = gvp.filter_volcanoes(name="Unnamed")
if len(unnamed) > 0:
    print(f"Found {len(unnamed)} unnamed volcanoes")
    print(f"First unnamed volcano: {unnamed[0].name}")

# Test elevation filtering
high_elevation = gvp.filter_volcanoes(min_elevation=3000)
print(f"Volcanoes above 3000m: {len(high_elevation)}")

# Test volcano type filtering
calderas = gvp.filter_volcanoes(volcano_type="Caldera")
print(f"Calderas: {len(calderas)}")

# Test getting a specific volcano by ID
specific_volcano = gvp.get_volcano_by_id(211060)
if specific_volcano:
    print(f"Volcano ID 211060: {specific_volcano.name}")
else:
    print("Volcano ID 211060 not found")