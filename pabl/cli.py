"""
Command-line interface for Pabl
"""

import argparse
import sys
from typing import List, Optional
from .core import ImageHandler

def create_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        description="Pabl - A fast, local image upload CLI tool"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload one or more images")
    upload_parser.add_argument(
        "files",
        nargs="+",
        help="One or more image files to upload"
    )
    upload_parser.add_argument(
        "--memory",
        action="store_true",
        help="Store images in temporary memory and display clickable path"
    )
    upload_parser.add_argument(
        "--open",
        action="store_true",
        help="Open the image automatically after upload"
    )
    
    # Move command
    move_parser = subparsers.add_parser("move", help="Move an image from one path to another (super optimized)")
    move_parser.add_argument(
        "source",
        help="Source image file path"
    )
    move_parser.add_argument(
        "destination",
        help="Destination path for the image"
    )
    
    # Drop command
    drop_parser = subparsers.add_parser("drop", help="Enter drop mode for image uploads")
    drop_parser.add_argument(
        "--timeout",
        type=int,
        default=0,
        help="Timeout in seconds (0 for no timeout)"
    )
    
    return parser

def open_file_native(path: str):
    import os
    import sys
    import subprocess
    try:
        if sys.platform.startswith('win'):
            os.startfile(path)
        elif sys.platform.startswith('darwin'):
            subprocess.run(['open', path], check=True)
        else:
            subprocess.run(['xdg-open', path], check=True)
        print(f"Opened image in default viewer: {path}")
    except Exception as e:
        print(f"Failed to open image: {e}")

def handle_upload(files: List[str], memory: bool = False, open_file: bool = False) -> None:
    """Handle the upload command."""
    handler = ImageHandler()
    for file in files:
        try:
            result = handler.process_image(file, memory=memory)
            print(f"✓ Copied to temp: {result['path']}")
            print(f"[Open image] {result['file_url']}")
            print(f"[File path] {result['path']}")
            if open_file:
                open_file_native(result['path'])
            if memory:
                print(f"✓ Loaded in memory: {result['path']}")
        except Exception as e:
            print(f"✗ Error processing {file}: {str(e)}", file=sys.stderr)

def handle_move(source: str, destination: str) -> None:
    """Handle the move command."""
    from .core import move_image
    try:
        move_image(source, destination)
        print(f"✓ Moved: {source} -> {destination}")
    except Exception as e:
        print(f"✗ Error moving {source}: {str(e)}", file=sys.stderr)

def handle_drop(timeout: Optional[int] = None) -> None:
    """Handle the drop command."""
    handler = ImageHandler()
    print("Drop mode activated. Drag and drop images here (Ctrl+C to exit)")
    
    try:
        while True:
            try:
                file_path = input("> ").strip()
                if file_path:
                    result = handler.process_image(file_path)
                    print(f"✓ Processed: {file_path}")
            except EOFError:
                break
    except KeyboardInterrupt:
        print("\nDrop mode deactivated")

def main() -> None:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == "upload":
        handle_upload(args.files, memory=getattr(args, 'memory', False), open_file=getattr(args, 'open', False))
    elif args.command == "move":
        handle_move(args.source, args.destination)
    elif args.command == "drop":
        handle_drop(args.timeout)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 