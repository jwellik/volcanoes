import math
from typing import Optional, Tuple, Dict, Any


class Volcano:
    """Represents a single volcano with all its properties and methods."""

    def __init__(self, data: Dict[str, Any]):
        """Initialize a Volcano object from a dictionary of data."""
        self._data = data
        self._process_data()

    def _process_data(self):
        """Process and clean the raw data."""
        # Handle unnamed volcanoes
        if self._data.get('VolcanoName', '').strip().lower() == 'unnamed':
            self._data['VolcanoName'] = f"Unnamed-{self._data['VolcanoNumber']}"

        # Convert numeric fields
        numeric_fields = ['VolcanoNumber', 'LastEruptionYear', 'Latitude', 'Longitude', 'Elevation']
        for field in numeric_fields:
            if field in self._data and self._data[field] != '':
                try:
                    if field == 'VolcanoNumber':
                        self._data[field] = int(self._data[field])
                    else:
                        self._data[field] = float(self._data[field])
                except (ValueError, TypeError):
                    self._data[field] = None

    @property
    def volcano_number(self) -> int:
        """Get the volcano number (unique identifier)."""
        return self._data.get('VolcanoNumber')

    @property
    def id(self) -> int:
        """Alias for volcano_number."""
        return self.volcano_number

    @property
    def name(self) -> str:
        """Get the volcano name."""
        return self._data.get('VolcanoName', '')

    @property
    def volcano_type(self) -> str:
        """Get the volcano type."""
        return self._data.get('VolcanoType', '')

    @property
    def country(self) -> str:
        """Get the country."""
        return self._data.get('Country', '')

    @property
    def region(self) -> str:
        """Get the region."""
        return self._data.get('Region', '')

    @property
    def subregion(self) -> str:
        """Get the subregion."""
        return self._data.get('Subregion', '')

    @property
    def lat(self) -> Optional[float]:
        """Get the latitude."""
        return self._data.get('Latitude')

    @property
    def latitude(self) -> Optional[float]:
        """Alias for lat."""
        return self.lat

    @property
    def lon(self) -> Optional[float]:
        """Get the longitude."""
        return self._data.get('Longitude')

    @property
    def longitude(self) -> Optional[float]:
        """Alias for lon."""
        return self.lon

    def get_elevation(self, units: str = "m") -> Optional[float]:
        """Get the elevation in specified units (m or ft)."""
        elev_m = self._data.get('Elevation')
        if elev_m is None:
            return None

        if units.lower() == "m":
            return elev_m
        elif units.lower() in ["ft", "feet"]:
            return elev_m * 3.28084
        else:
            raise ValueError("Units must be 'm' or 'ft'")

    @property
    def elevation(self) -> Optional[float]:
        "Get the elevation in m."
        return self.get_elevation()

    @property
    def elev(self) -> Optional[float]:
        """Alias for elevation."""
        return self.elevation

    @property
    def origin(self) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Get (latitude, longitude, elevation_m) as a tuple."""
        return (self.lat, self.lon, self.get_elevation())

    @property
    def last_eruption_year(self) -> Optional[float]:
        """Get the last eruption year."""
        return self._data.get('LastEruptionYear')

    @property
    def geological_summary(self) -> str:
        """Get the geological summary."""
        return self._data.get('GeologicalSummary', '')

    @property
    def tectonic_setting(self) -> str:
        """Get the tectonic setting."""
        return self._data.get('TectonicSetting', '')

    @property
    def geologic_epoch(self) -> str:
        """Get the geologic epoch."""
        return self._data.get('GeologicEpoch', '')

    @property
    def evidence_category(self) -> str:
        """Get the evidence category."""
        return self._data.get('EvidenceCategory', '')

    @property
    def major_rock_type(self) -> str:
        """Get the major rock type."""
        return self._data.get('MajorRockType', '')

    @property
    def last_update_date(self) -> str:
        """Get the last update date."""
        return self._data.get('LastUpdateDate', '')

    @property
    def remarks(self) -> str:
        """Get the remarks."""
        return self._data.get('Remarks', '')

    @property
    def eruption_history(self):
        """Placeholder for future EruptionHistory class."""
        # This will be implemented when you add the EruptionHistory class
        return None

    def distance_to(self, lat: float, lon: float) -> float:
        """Calculate distance to a point in kilometers using Haversine formula."""
        if self.lat is None or self.lon is None:
            return float('inf')

        return self._haversine_distance(self.lat, self.lon, lat, lon)

    def _haversine_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate the great circle distance between two points using Haversine formula."""
        R = 6371  # Earth's radius in kilometers

        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    def simple_plot(self):
        """Plot the volcano on a simple map."""
        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as patches
        except ImportError:
            print("Matplotlib is required for plotting. Install with: pip install matplotlib")
            return

        if self.lat is None or self.lon is None:
            print(f"Cannot plot {self.name}: missing coordinates")
            return

        # Simple plotting - volcano in center with 50km extent
        extent_deg = 0.45  # Approximately 50km at mid-latitudes

        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot volcano as a red triangle
        ax.scatter(self.lon, self.lat, c='orange', s=100, marker='^',
                   edgecolors="black",
                   label=f'{self.name}', zorder=5)

        # Set map extent
        ax.set_xlim(self.lon - extent_deg, self.lon + extent_deg)
        ax.set_ylim(self.lat - extent_deg, self.lat + extent_deg)

        # Add grid and labels
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title(f'{self.name} ({self.country})')
        ax.legend()

        # # Add basic info
        # info_text = f"Elevation: {self.get_elevation() :.0f}m" if self.get_elevation() else "Elevation: Unknown"
        # if self.last_eruption_year:
        #     info_text += f"\nLast Eruption: {int(self.last_eruption_year)}"
        #
        # ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
        #         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        plt.tight_layout()
        plt.show()

    def plot(self, extent_km=50.0):

        try:
            import matplotlib.pyplot as plt
            import matplotlib.patches as patches
            import matplotlib.pyplot as plt
            import cartopy.crs as ccrs
            from cartopy.io.img_tiles import GoogleTiles
        except ImportError:
            print("Matplotlib and Cartopy are required for advanced plotting. Install with: pip install matplotlib")
            self.simple_plot()

        from obspy.geodetics import kilometers2degrees as km2dd
        from volcanoes.utils.plotting import get_zoom_level_interpolated

        if self.lat is None or self.lon is None:
            print(f"Cannot plot {self.name}: missing coordinates")
            return

        extent_deg = km2dd(extent_km)
        zoom_level = get_zoom_level_interpolated(extent_km)

        tiler = GoogleTiles(style="satellite")
        # tiler = GoogleTiles(style="terrain")  # "street" works, "terrain" appears not to work
        mercator = tiler.crs

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1, projection=mercator)
        ax.set_extent([self.lon - extent_deg, self.lon + extent_deg,
                       self.lat - extent_deg, self.lat + extent_deg],
                      crs=ccrs.PlateCarree())
        ax.add_image(tiler, zoom_level)
        # ax.coastlines('10m')

        # Plot volcano as a red triangle
        ax.scatter(self.lon, self.lat, c='orange', s=100, marker='^',
                   edgecolors="black",
                   label=f'{self.name}', zorder=5,
                   transform=ccrs.Geodetic(),
                   )
        ax.legend()

        # Axis grid lines
        gl = ax.gridlines(draw_labels=True)  # JJW
        gl.top_labels = False  # JJW
        gl.right_labels = False  # JJW
        plt.tight_layout()

        plt.savefig("./volcano.png")

    def __str__(self) -> str:
        """String representation of the volcano."""
        elev_str = f"{self.get_elevation() :.0f}m" if self.get_elevation() else "Unknown"
        return f"Volcano ({self.name}, {self.country}, {elev_str})"

    def __repr__(self) -> str:
        """Detailed representation of the volcano."""
        return f"Volcano(id={self.id}, name='{self.name}', country='{self.country}')"

    def _wrap_text(self, text, line_length=80):
        import textwrap
        return textwrap.wrap(text, width=line_length)

    def print(self):
        """
        AWU (Indonesia) | 267040
        Location  : 3.689, 125.447, 1318m
        Region 	  : Sanghihe Volcanic Arc
        Volc Type : Composite | Stratovolcano
        Last Known Eruption : 2004 CE
        Eruptive History:
        2004 CE :
        1992 CE :
        """

        print(f"{self.name.upper()} ({self.country}) | {self.id}")
        print(f"{self.region}")
        print(f"({self.lat}, {self.lon}, {self.elev})")
        print(f"{self.tectonic_setting} | {self.volcano_type}")
        print(f"{self.major_rock_type}")
        print(f"Last Known Eruption: {int(self.last_eruption_year)}")
        print("Geologic Summary:")
        geo_sum = self._wrap_text(self.geological_summary)
        [print(" ", line) for line in geo_sum]
        print()
