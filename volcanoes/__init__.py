# File: volcanoes/__init__.py (Main package __init__.py)
"""
Volcanoes: A Python package for working with GVP volcano data
"""

from .core.gvp import GVP
from .core.volcano import Volcano
from .core.volcano_set import VolcanoSet

__version__ = "0.1.0"
__all__ = ["GVP", "Volcano", "VolcanoSet"]

# Optional: Add package-level documentation
__author__ = "Your Name"
__email__ = "jwellik@usgs.gov"
__description__ = "A Python package for working with GVP volcano data"