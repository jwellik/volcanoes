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
