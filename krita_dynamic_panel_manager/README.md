# Krita Dynamic Panel Manager Plugin

A powerful plugin for Krita that enables dynamic management of dock panels, allowing users to create and organize up to 8 separate panel columns with intuitive drag-and-drop functionality.

## Features

- Create up to 8 separate panel columns horizontally
- Drag-and-drop panels between columns
- Resizable panels with modern styling
- Save and load panel layouts
- Intuitive user interface with visual feedback
- Full compatibility with Krita 5.2.9

## Installation

1. Close Krita if it's running
2. Copy the `krita_dynamic_panel_manager` folder to Krita's resource folder:
   - Linux: `~/.local/share/krita/pykrita/`
   - Windows: `%APPDATA%\krita\pykrita\`
   - macOS: `~/Library/Application Support/Krita/pykrita/`
3. Enable the plugin in Krita:
   - Open Krita
   - Go to Settings → Configure Krita
   - Navigate to Python Plugin Manager
   - Check "Dynamic Panel Manager"
   - Click OK
   - Restart Krita

## Usage

### Basic Operations

1. **Adding a Panel Column**
   - Go to View → Panel Manager → Add Panel Column
   - Or use the keyboard shortcut (if configured)

2. **Moving Panels**
   - Click and drag a panel to move it
   - Drop it in another column to reposition

3. **Resizing Panels**
   - Use the resize grip at the bottom-right corner of each panel
   - Drag to adjust the size

4. **Removing Panels**
   - Go to View → Panel Manager → Remove Panel Column
   - Removes the last added column

### Layout Management

- **Reset Layout**
  - Go to View → Panel Manager → Reset Layout
  - Returns to the default single-column layout

## Development

### Requirements

- Krita 5.2.9 or later
- Python 3.x
- PyQt5

### Project Structure

```
krita_dynamic_panel_manager/
├── __init__.py                 # Plugin entry point
├── panel_manager_extension.py  # Main extension class
├── drag_drop_panel_widget.py   # Panel widget with drag-drop
├── panel_layout_manager.py     # Layout management
└── manifest.json              # Plugin metadata
```

### Building from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/krita-dynamic-panel-manager.git
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run tests:
   ```bash
   python -m unittest discover tests
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Acknowledgments

- Krita Development Team for the excellent Python API
- Contributors and testers who helped improve the plugin

## Troubleshooting

### Common Issues

1. **Plugin not appearing in Krita**
   - Verify the installation path
   - Check if Python plugins are enabled in Krita
   - Look for error messages in Krita's Python console

2. **Panels not dragging properly**
   - Ensure you're running a compatible Krita version
   - Check if any other plugins are conflicting

3. **Layout not saving**
   - Verify write permissions in the configuration directory
   - Check available disk space

### Getting Help

- Open an issue on GitHub
- Visit the Krita forums
- Check the Krita documentation

## Version History

- 1.0.0
  - Initial release
  - Basic panel management functionality
  - Drag-and-drop support
  - Layout saving/loading

## Future Plans

- Additional panel customization options
- Enhanced visual feedback during drag operations
- Panel grouping functionality
- Layout templates
- Performance optimizations
