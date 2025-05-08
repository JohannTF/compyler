"""
Utilities module for Compyler.
"""

# Import all functions to expose
from .file_handler import read_file

# Define what gets imported with "from src.utils import *"
__all__ = [
    'read_file',
]
