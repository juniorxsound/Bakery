# Bakery 🧑🏼‍🍳 🥐 ✨

A Blender add-on that simplifies texture baking

![Bakery](https://github.com/juniorxsound/bakery/blob/main/docs/bakery_ui.png?raw=true)

## Installation

1. Download the latest release from the [releases page](https://github.com/juniorxsound/bakery/releases)
2. Open Blender
3. Go to Edit > Preferences > Add-ons
4. Click "Install" and select the downloaded zip file
5. Enable the add-on by checking the box next to "Bakery"

## Usage

1. Select the object you want to bake textures for
2. Open the Sidebar (N key) and find the "Bake Tools" tab
3. Configure your bake settings:
   - Select the bake type (Combined, AO, Normal, etc.)
   - Set the texture resolution
   - Choose a save folder for the baked textures
4. Click "Bake Texture" to start the baking process
5. Monitor the progress in the status bar
6. Once complete, the baked texture will be saved to your specified folder

### Supported Bake Types

- **Combined**: Bakes all textures into a single image
- **Ambient Occlusion**: Bakes ambient occlusion map
- **Normal**: Bakes normal map (using tangent space)
- **Roughness**: Bakes roughness map
- **Metallic**: Bakes metallic map
- **Emission**: Bakes emission map

## Development

### Project Structure

```
bakery/
├── __init__.py      # Main add-on file with registration and properties
├── ops.py          # Operator definitions
├── utils.py        # Utility functions for baking
└── panels.py       # UI panel definitions
```

### Setting Up Development Environment

1. Clone the repository:

   ```bash
   git clone https://github.com/juniorxsound/bakery.git
   ```

2. Create a symbolic link to your Blender addons folder:

   ```bash
   # On macOS
   ln -s /path/to/bakery ~/Library/Application\ Support/Blender/3.6/scripts/addons/bakery

   # On Windows
   mklink /D "C:\Users\YourUsername\AppData\Roaming\Blender Foundation\Blender\3.6\scripts\addons\bakery" "C:\path\to\bakery"
   ```

3. Enable the add-on in Blender's preferences

### Key Components

#### Properties (`__init__.py`)

- `bake_type`: Enum property for selecting bake type
- `bake_resolution`: Int property for texture resolution
- `bake_save_path`: String property for save folder path

#### Operators (`ops.py`)

- `BAKE_OT_bake_texture`: Main baking operator with modal execution for progress tracking

#### Utilities (`utils.py`)

- `setup_bake_settings`: Configures bake settings based on type
- `prepare_material_for_baking`: Sets up material nodes for baking
- `create_or_get_image`: Creates or retrieves image for baking
- `save_baked_image`: Saves baked texture with automatic naming
- `setup_render_engine`: Configures render engine and GPU settings

## Contributing

Contributions are welcomed! Here's how you can help:

1. Fork the repository
2. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- Report bugs on the [GitHub Issues page](https://github.com/juniorxsound/bakery/issues)
