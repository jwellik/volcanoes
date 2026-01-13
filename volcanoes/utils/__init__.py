"""
Utility functions for the volcanoes package
"""

from .distance import haversine_distance
from .plotting import check_matplotlib

__all__ = ["haversine_distance", "check_matplotlib"]