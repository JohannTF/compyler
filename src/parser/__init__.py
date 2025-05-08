"""
Syntactic analysis module for Compyler.
"""

# Import all classes and functions to expose
from .parser import Parser

# Define what gets imported with "from src.parser import *"
__all__ = [
    'Parser',
]
