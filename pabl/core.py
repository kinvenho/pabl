"""
Core functionality for Pabl image handling
"""

import os
from pathlib import Path
from typing import Union, Dict, Any

class ImageHandler:
    """Handles image processing and validation."""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    
    def __init__(self):
        """Initialize the ImageHandler."""
        self.temp_dir = Path.home() / '.pabl' / 'temp'
        self._ensure_temp_dir()
    
    def _ensure_temp_dir(self) -> None:
        """Ensure the temporary directory exists."""
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def _validate_image_path(self, file_path: Union[str, Path]) -> Path:
        """Validate that the file exists and is an image."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported image format: {path.suffix}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
            )
        
        return path
    
    def process_image(self, file_path: Union[str, Path]) -> Dict[str, Any]:
        """
        Process an image file.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Dict containing processed image information
        """
        path = self._validate_image_path(file_path)
        
        # For now, just return basic file information
        # This will be expanded based on future requirements
        return {
            'filename': path.name,
            'size': path.stat().st_size,
            'format': path.suffix.lower()[1:],
            'path': str(path.absolute())
        }
    
    def cleanup(self) -> None:
        """Clean up temporary files."""
        import shutil
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir) 