"""
Solo Leveling Downloader Package

This package provides tools to:
- Generate chapter URLs
- Download and process manga images
- Merge images into panels
- Export cleaned outputs as PDF or EPUB
"""

__version__ = "1.0.0"
__author__ = "bob-bee"
__email__ = "geniusfaker@gmail.com"

# Expose pipeline functions for easier import
from .url_generator import generate_urls
from .downloader import download_all
from .converter import convert_all
