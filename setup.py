from setuptools import setup, find_packages

setup(
    name="volcanoes",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "matplotlib>=3.0.0",
        "requests>=2.25.0",
    ],
    extras_require={
        'dev': ['pytest', 'pytest-cov', 'black', 'flake8'],
    },
    author="Your Name",
    author_email="jwellik@usgs.gov",
    description="A Python package for working with GVP volcano data",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    include_package_data=True,
    # Note: CSV data files are no longer bundled. Data is downloaded and cached on first use.
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)