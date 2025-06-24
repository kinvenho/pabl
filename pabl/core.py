"""
Core functionality for Pabl image handling
"""

import os
from pathlib import Path
from typing import Union, Dict, Any, Optional
import atexit
import shutil
import urllib.parse

class ImageHandler:
    """Handles image processing and validation."""
    
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    _memory_store: Dict[str, bytes] = {}
    _temp_dir_registered: bool = False
    
    def __init__(self):
        """Initialize the ImageHandler."""
        self.temp_dir = Path.home() / '.pabl' / 'tmp'
        self._ensure_temp_dir()
        if not ImageHandler._temp_dir_registered:
            atexit.register(self.cleanup)
            ImageHandler._temp_dir_registered = True
    
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
    
    def process_image(self, file_path: Union[str, Path], memory: bool = False) -> Dict[str, Any]:
        """
        Process an image file: always copy to temp dir, optionally load into memory.
        """
        path = self._validate_image_path(file_path)
        temp_path = self.temp_dir / path.name
        shutil.copy2(path, temp_path)
        file_url_path = str(temp_path.absolute()).replace('\\', '/')
        file_url = f"file:///{urllib.parse.quote(file_url_path)}"
        info = {
            'filename': temp_path.name,
            'size': temp_path.stat().st_size,
            'format': temp_path.suffix.lower()[1:],
            'path': str(temp_path.absolute()),
            'file_url': file_url
        }
        if memory:
            with open(temp_path, 'rb') as f:
                self._memory_store[str(temp_path)] = f.read()
        return info
    
    def cleanup(self) -> None:
        """Clean up temporary files."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

def move_image(source: Union[str, Path], destination: Union[str, Path]) -> None:
    """Move an image from source to destination using an optimized method."""
    src = Path(source)
    dst = Path(destination)
    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {source}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    import os
    try:
        os.replace(str(src), str(dst))  # atomic move if possible
    except Exception:
        import shutil
        shutil.move(str(src), str(dst)) 