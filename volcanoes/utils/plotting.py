# File: volcanoes/utils/plotting.py
"""Plotting utilities for volcano visualization."""

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

def check_matplotlib():
    """Check if matplotlib is available."""
    if not HAS_MATPLOTLIB:
        raise ImportError("Matplotlib is required for plotting. Install with: pip install matplotlib")


# Dictionary mapping extent_km to appropriate zoom levels for Google Tiles
ZOOM_LEVELS = {
    # Very close up - building/structure level detail
    0.1: 18,  # ~100m extent
    0.5: 17,  # ~500m extent
    1.0: 16,  # ~1km extent
    2.0: 15,  # ~2km extent

    # Local area - city block to neighborhood level
    5.0: 14,  # ~5km extent
    10.0: 13,  # ~10km extent
    20.0: 12,  # ~20km extent

    # Regional - city to county level
    50.0: 11,  # ~50km extent (your default)
    100.0: 10,  # ~100km extent
    200.0: 9,  # ~200km extent

    # Large scale - state/province level
    500.0: 8,  # ~500km extent
    1000.0: 7,  # ~1000km extent
    2000.0: 6,  # ~2000km extent

    # Continental scale
    5000.0: 5,  # ~5000km extent
    10000.0: 4,  # ~10000km extent
}


def get_zoom_level_basic(extent_km):
    """
    Get appropriate zoom level for given extent in kilometers.

    Args:
        extent_km (float): Extent in kilometers

    Returns:
        int: Zoom level (4-18)
    """
    # Find the closest extent key
    closest_extent = min(ZOOM_LEVELS.keys(), key=lambda x: abs(x - extent_km))
    return ZOOM_LEVELS[closest_extent]


# Alternative function for more precise interpolation
def get_zoom_level_interpolated(extent_km):
    """
    Get zoom level with linear interpolation between defined points.

    Args:
        extent_km (float): Extent in kilometers

    Returns:
        int: Zoom level (4-18)
    """
    import numpy as np

    extents = sorted(ZOOM_LEVELS.keys())
    zooms = [ZOOM_LEVELS[ext] for ext in extents]

    # Clamp to bounds
    if extent_km <= extents[0]:
        return zooms[0]
    elif extent_km >= extents[-1]:
        return zooms[-1]

    # Linear interpolation and round to nearest integer
    zoom = np.interp(extent_km, extents, zooms)
    return int(round(zoom))