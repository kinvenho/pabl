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
    
    # Drop command
    drop_parser = subparsers.add_parser("drop", help="Enter drop mode for image uploads")
    drop_parser.add_argument(
        "--timeout",
        type=int,
        default=0,
        help="Timeout in seconds (0 for no timeout)"
    )
    
    return parser

def handle_upload(files: List[str]) -> None:
    """Handle the upload command."""
    handler = ImageHandler()
    for file in files:
        try:
            result = handler.process_image(file)
            print(f"✓ Processed: {file}")
        except Exception as e:
            print(f"✗ Error processing {file}: {str(e)}", file=sys.stderr)

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
        handle_upload(args.files)
    elif args.command == "drop":
        handle_drop(args.timeout)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main() 