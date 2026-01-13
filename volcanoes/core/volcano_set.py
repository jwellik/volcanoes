# File: volcanoes/core/volcano_set.py
from typing import List, Optional, Union, Iterator
import math


class VolcanoSet:
    """A collection of volcanoes with filtering and analysis methods."""

    def __init__(self, volcanoes: List['Volcano']):
        """Initialize with a list of Volcano objects."""
        self._volcanoes = volcanoes

    def __len__(self) -> int:
        """Return the number of volcanoes in the set."""
        return len(self._volcanoes)

    def __getitem__(self, index: Union[int, slice]) -> Union['Volcano', 'VolcanoSet']:
        """Get volcano(es) by index."""
        if isinstance(index, slice):
            return VolcanoSet(self._volcanoes[index])
        return self._volcanoes[index]

    def __iter__(self) -> Iterator['Volcano']:
        """Iterate over volcanoes."""
        return iter(self._volcanoes)

    @property
    def volcanoes(self) -> List['Volcano']:
        """Get the list of volcanoes."""
        return self._volcanoes

    def filter_by_country(self, country: str) -> 'VolcanoSet':
        """Filter volcanoes by country."""
        filtered = [v for v in self._volcanoes if v.country.lower() == country.lower()]
        return VolcanoSet(filtered)

    def filter_by_type(self, volcano_type: str) -> 'VolcanoSet':
        """Filter volcanoes by type."""
        filtered = [v for v in self._volcanoes if volcano_type.lower() in v.volcano_type.lower()]
        return VolcanoSet(filtered)

    def filter_by_elevation_range(self, min_elev: float, max_elev: float) -> 'VolcanoSet':
        """Filter volcanoes by elevation range."""
        filtered = []
        for v in self._volcanoes:
            elev = v.get_elevation()
            if elev is not None and min_elev <= elev <= max_elev:
                filtered.append(v)
        return VolcanoSet(filtered)

    def sort_by_distance(self, lat: float, lon: float) -> 'VolcanoSet':
        """Sort volcanoes by distance from a point."""
        sorted_volcanoes = sorted(self._volcanoes, key=lambda v: v.distance_to(lat, lon))
        return VolcanoSet(sorted_volcanoes)

    def sort_by_elevation(self, reverse: bool = True) -> 'VolcanoSet':
        """Sort volcanoes by elevation.
        
        Args:
            reverse: If True, sort descending (highest first). If False, sort ascending.
        """
        sorted_volcanoes = sorted(
            self._volcanoes,
            key=lambda v: v.get_elevation() if v.get_elevation() is not None else float('-inf'),
            reverse=reverse
        )
        return VolcanoSet(sorted_volcanoes)

    def within_radius(self, lat: float, lon: float, radius_km: float) -> 'VolcanoSet':
        """Get volcanoes within a radius of a point."""
        filtered = [v for v in self._volcanoes if v.distance_to(lat, lon) <= radius_km]
        return VolcanoSet(filtered)

    def get_lats(self):
        return [v.lat for v in self._volcanoes if v.lat is not None]

    def get_lons(self):
        return [v.lon for v in self._volcanoes if v.lon is not None]

    def get_elevs(self):
        return [v.elev for v in self._volcanoes if v.elev is not None]

    def print(self, limit: Optional[int] = None):
        """Print information about volcanoes in the set."""
        volcs_to_print = self._volcanoes[:limit] if limit else self._volcanoes

        print(f"VolcanoSet with {len(self._volcanoes)} volcanoes:")
        print("-" * 80)

        for i, volcano in enumerate(volcs_to_print):
            elev_str = f"{volcano.get_elevation() :4.0f}m" if volcano.get_elevation() else "----m"
            origin_str = f"{volcano.lat:>+6.3f}, {volcano.lon:>+7.3f}, {elev_str}"
            elev_str = f"{volcano.get_elevation() :.0f}m" if volcano.get_elevation() else "Unknown"
            last_eruption = f"{int(volcano.last_eruption_year)}" if volcano.last_eruption_year else "Unknown"

            print(f"{i + 1:3d}. {volcano.name:<30} | {volcano.country:<15} | "
                  f"{origin_str:>22} | Last: {last_eruption}")

        if limit and len(self._volcanoes) > limit:
            print(f"... and {len(self._volcanoes) - limit} more")

    def simple_plot(self):
        """Plot all volcanoes in the set on a simple map."""
        try:
            import matplotlib.pyplot as plt
        except ImportError:
            print("Matplotlib is required for plotting. Install with: pip install matplotlib")
            return

        if not self._volcanoes:
            print("No volcanoes to plot")
            return

        # Get coordinates of all volcanoes
        lats = [v.lat for v in self._volcanoes if v.lat is not None]
        lons = [v.lon for v in self._volcanoes if v.lon is not None]

        if not lats or not lons:
            print("No volcanoes with valid coordinates to plot")
            return

        fig, ax = plt.subplots(figsize=(12, 8))

        # Plot volcanoes
        ax.scatter(lons, lats, c="orange", s=60, marker='^',
                   alpha=0.8, edgecolors='black', linewidth=0.8)

        # Set map extent with some padding
        lat_range = max(lats) - min(lats)
        lon_range = max(lons) - min(lons)
        padding = max(lat_range, lon_range) * 0.1

        ax.set_xlim(min(lons) - padding, max(lons) + padding)
        ax.set_ylim(min(lats) - padding, max(lats) + padding)

        # Add grid and labels
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title(f'Volcano Locations ({len(self._volcanoes)} volcanoes)')

        # Add country info if all from same country
        countries = list(set(v.country for v in self._volcanoes))
        if len(countries) == 1:
            ax.set_title(f'Volcanoes in {countries[0]} ({len(self._volcanoes)} volcanoes)')

        plt.tight_layout()
        plt.show()

    def plot(self):

        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as patches
            import cartopy.crs as ccrs
            from cartopy.io.img_tiles import GoogleTiles
        except ImportError:
            print("Matplotlib and Cartopy are required for advanced plotting. Install with: pip install matplotlib")
            self.simple_plot()
            return

        import numpy as np
        from volcanoes.utils.plotting import get_zoom_level_interpolated

        if not self._volcanoes:
            print("No volcanoes to plot")
            return

        # Get coordinates of all volcanoes
        lats = [v.lat for v in self._volcanoes if v.lat is not None]
        lons = [v.lon for v in self._volcanoes if v.lon is not None]

        if not lats or not lons:
            print("No volcanoes with valid coordinates to plot")
            return

        # Set map extent with some padding
        lat_range = max(lats) - min(lats)
        lon_range = max(lons) - min(lons)
        padding = max(lat_range, lon_range) * 0.1

        # Convert degrees to kilometers: 1 degree ≈ 111.32 km
        # For longitude, account for latitude: 1 degree longitude ≈ 111.32 * cos(lat) km
        avg_lat = np.radians(np.mean(lats))
        lat_range_km = lat_range * 111.32
        lon_range_km = lon_range * 111.32 * np.cos(avg_lat)
        extent_km = np.maximum(lat_range_km, lon_range_km)
        zoom_level = get_zoom_level_interpolated(extent_km)

        tiler = GoogleTiles(style="satellite")
        # tiler = GoogleTiles(style="terrain")  # "street" works, "terrain" appears not to work
        mercator = tiler.crs

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection=mercator)
        ax.set_extent([min(lons) - padding, max(lons) + padding,
                       min(lats) - padding, max(lats) + padding],
                      crs=ccrs.PlateCarree())
        ax.add_image(tiler, zoom_level)
        # ax.coastlines('10m')

        # Plot volcanoes
        ax.scatter(lons, lats, c="orange", s=60, marker='^',
                   alpha=0.8, edgecolors='black', linewidth=0.8, zorder=5,
                   transform=ccrs.Geodetic())

        # Axis grid lines
        gl = ax.gridlines(draw_labels=True)
        gl.top_labels = False
        gl.right_labels = False
        plt.tight_layout()

        # Add country info if all from same country
        countries = list(set(v.country for v in self._volcanoes))
        if len(countries) == 1:
            ax.set_title(f'Volcanoes in {countries[0]} ({len(self._volcanoes)} volcanoes)')

        plt.tight_layout()
        plt.savefig("./volcano_set.png")

    def summary_stats(self) -> dict:
        """Get summary statistics for the volcano set."""
        elevations = [v.get_elevation() for v in self._volcanoes if v.get_elevation() is not None]
        countries = [v.country for v in self._volcanoes]
        types = [v.volcano_type for v in self._volcanoes]

        return {
            'total_volcanoes': len(self._volcanoes),
            'countries': len(set(countries)),
            'volcano_types': len(set(types)),
            'avg_elevation': sum(elevations) / len(elevations) if elevations else None,
            'max_elevation': max(elevations) if elevations else None,
            'min_elevation': min(elevations) if elevations else None,
        }

    def export_to_csv(self, output_path: str) -> str:
        """Export volcano data to CSV.
        
        Args:
            output_path: Path to output CSV file
            
        Returns:
            Path to the exported file
        """
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if not self._volcanoes:
                return output_path
            
            # Get fieldnames from first volcano
            fieldnames = list(self._volcanoes[0]._data.keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for volcano in self._volcanoes:
                writer.writerow(volcano._data)
        
        print(f"Exported {len(self._volcanoes)} volcanoes to CSV: {output_path}")
        return output_path
    
    def export_to_geojson(self, output_path: str) -> str:
        """Export volcano data to GeoJSON.
        
        Args:
            output_path: Path to output GeoJSON file
            
        Returns:
            Path to the exported file
        """
        import json
        
        features = []
        for volcano in self._volcanoes:
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