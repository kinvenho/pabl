"""
Tests for Pabl core functionality
"""

import pytest
from pathlib import Path
from pabl.core import ImageHandler

def test_image_handler_init():
    """Test ImageHandler initialization."""
    handler = ImageHandler()
    assert handler.temp_dir.exists()
    assert handler.temp_dir.is_dir()

def test_validate_image_path_not_found():
    """Test validation of non-existent file."""
    handler = ImageHandler()
    with pytest.raises(FileNotFoundError):
        handler._validate_image_path("nonexistent.jpg")

def test_validate_image_path_invalid_format():
    """Test validation of unsupported format."""
    handler = ImageHandler()
    # Create a temporary text file
    temp_file = Path("temp.txt")
    temp_file.touch()
    
    try:
        with pytest.raises(ValueError):
            handler._validate_image_path(temp_file)
    finally:
        temp_file.unlink()

# Add more tests as needed 