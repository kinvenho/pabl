"""
Pabl - A fast, local image upload CLI tool
"""

__version__ = "0.1.0"

from .core import ImageHandler
from .cli import main

__all__ = ['ImageHandler', 'main'] 