# Pabl

A fast, local image upload CLI tool designed for seamless integration with image processing workflows.

## Installation

```bash
pip install pabl
```

## Usage

```bash
# Upload a single image (copies to temp directory)
pabl upload "C:\path\to\image.png"

# Upload and open in default image viewer
pabl upload --open "C:\path\to\image.png"

# Upload and store in memory (for advanced integrations)
pabl upload --memory "C:\path\to\image.png"

# Move an image (super optimized)
pabl move "C:\path\to\image.png" "C:\new\location\image.png"

# Enter drop mode to accept dragged images or pasted paths
pabl drop

# Get help
pabl --help
```

## Features

- Fast local image handling
- All uploads are copied to a temp directory (`~/.pabl/tmp/` or `%USERPROFILE%\.pabl\tmp\`)
- Temp directory is cleaned up automatically when the process exits
- `--open` flag opens the image in your system's default image viewer
- `--memory` flag loads the image into memory for advanced integrations
- Move images locally with `pabl move`
- Drag-and-drop support via `pabl drop` command
- Cross-platform compatibility (Windows, macOS, Linux)
- Designed for integration with other tools

## Development

To contribute to Pabl:

1. Clone the repository
2. Install development dependencies: `pip install -e .`
3. Make your changes
4. Submit a pull request

## License

MIT License 
=======
# pabl
open-source, terminal-based tool in Python designed for fast, local image uploads
