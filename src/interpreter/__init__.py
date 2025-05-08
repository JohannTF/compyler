"""
Interpreter module for Compyler.
"""

# Import all functions to expose
from .repl import start_repl

# Define what gets imported with "from src.interpreter import *"
__all__ = [
    'start_repl',
]
