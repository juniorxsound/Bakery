bl_info = {
    "name": "Bakery",
    "author": "Or Fleisher <contact@orfleisher.com>",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Bakery",
    "description": "Advanced texture baking tools for Blender",
    "warning": "",
    "doc_url": "https://github.com/juniorxsound/bakery",
    "category": "Baking",
}

import bpy
from bpy.props import (
    StringProperty,
    EnumProperty,
    IntProperty,
)

from .panels import BAKE_PT_main_panel
from .ops import BAKE_OT_bake_texture

# Define bake types
BAKE_TYPES = [
    ('COMBINED', "Combined", "Bake all textures combined"),
    ('AO', "Ambient Occlusion", "Bake ambient occlusion"),
    ('NORMAL', "Normal", "Bake normal map"),
    ('ROUGHNESS', "Roughness", "Bake roughness map"),
    ('METALLIC', "Metallic", "Bake metallic map"),
    ('EMIT', "Emission", "Bake emission map"),
]

# Registration
classes = (
    BAKE_PT_main_panel,
    BAKE_OT_bake_texture,
)

def register():
    print("Registering Bakery addon...")
    print(f"Classes to register: {[cls.__name__ for cls in classes]}")  # Debug print
    
    # Register properties
    bpy.types.Scene.bake_type = EnumProperty(
        name="Bake Type",
        description="Type of texture to bake",
        items=BAKE_TYPES,
        default='COMBINED'
    )
    
    bpy.types.Scene.bake_resolution = IntProperty(
        name="Resolution",
        description="Texture resolution (width and height)",
        default=2048,
        min=32,
        max=16384
    )
    
    bpy.types.Scene.bake_save_path = StringProperty(
        name="Save Folder",
        description="Folder to save the baked textures",
        default="",
        subtype='DIR_PATH'  # This makes it a folder selector
    )
    
    # Register classes
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
            print(f"Registered class: {cls.__name__}")
        except Exception as e:
            print(f"Error registering class {cls.__name__}: {str(e)}")
            raise

def unregister():
    print("Unregistering Bakery addon...")
    
    # Remove properties
    del bpy.types.Scene.bake_type
    del bpy.types.Scene.bake_resolution
    del bpy.types.Scene.bake_save_path
    
    # Unregister classes
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
            print(f"Unregistered class: {cls.__name__}")
        except Exception as e:
            print(f"Error unregistering class {cls.__name__}: {str(e)}")
            raise

if __name__ == "__main__":
    register()
