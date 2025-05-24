# File: setup.py (optional, for pip installation)
from setuptools import setup, find_packages

setup(
    name="volcanoes",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.0.0",  # Optional, for plotting
    ],
    author="Your Name",
    author_email="jwellik@usgs.gov",
    description="A Python package for working with GVP volcano data",
    long_description="A comprehensive package for loading, filtering, and analyzing volcano data from the Global Volcanism Program.",
    python_requires=">=3.7",
    include_package_data=True,
    package_data={
        'volcanoes': ['data/*.csv'],
    },
)
