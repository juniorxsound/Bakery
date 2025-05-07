import os
import bpy

def setup_bake_settings(context, bake_type):
    """Set up the bake settings for the given bake type"""
    context.scene.cycles.bake_type = bake_type
    
    # Additional settings for specific bake types
    if bake_type == 'NORMAL':
        context.scene.render.bake.use_selected_to_active = False
        context.scene.render.bake.normal_space = 'TANGENT'
    elif bake_type == 'AO':
        context.scene.cycles.samples = 128

def prepare_material_for_baking(mat):
    """Prepare a material for baking by ensuring it uses nodes and has an image texture node"""
    # Ensure the material uses nodes
    if not mat.use_nodes:
        mat.use_nodes = True
    
    # Find or create Image Texture node
    image_node = None
    for node in mat.node_tree.nodes:
        if node.type == 'TEX_IMAGE':
            image_node = node
            break
    
    if not image_node:
        image_node = mat.node_tree.nodes.new('ShaderNodeTexImage')
    
    return image_node

def create_or_get_image(obj_name, bake_type, resolution):
    """Create a new image or get an existing one for baking"""
    image_name = f"{obj.name}_{bake_type.lower()}"
    image = bpy.data.images.get(image_name)
    if not image:
        image = bpy.data.images.new(image_name, resolution, resolution)
    return image

def save_baked_image(image, save_folder, obj_name, bake_type):
    """Save the baked image to the specified folder with an appropriate filename"""
    if save_folder:
        # Create the folder if it doesn't exist
        os.makedirs(save_folder, exist_ok=True)
        
        # Generate filename based on object name and bake type
        filename = f"{obj_name}_{bake_type.lower()}.png"
        filepath = os.path.join(save_folder, filename)
        
        # Save the image
        image.save_render(filepath)
        return True, filepath
    return False, None

def setup_render_engine(context):
    """Set up the render engine for baking and return the original engine"""
    current_engine = context.scene.render.engine
    context.scene.render.engine = 'CYCLES'
    
    # Try to set up GPU rendering
    setup_gpu_rendering(context)
    
    return current_engine

def setup_gpu_rendering(context):
    """Set up GPU rendering if available, fall back to CPU if not"""
    
    # check CUDA/OptiX
    has_cuda = False
    has_optix = False
    
    for device in bpy.context.preferences.addons['cycles'].preferences.get_device_types(context):
        print(f"Found device: {device}")  # Debug print
        if device[0] == 'CUDA':
            has_cuda = True
        elif device[0] == 'OPTIX':
            has_optix = True
    
    # Set compute device type
    if has_optix:
        context.scene.cycles.device = 'GPU'
        context.scene.cycles.prefer_optix = True
    elif has_cuda:
        context.scene.cycles.device = 'GPU'
        context.scene.cycles.prefer_optix = False
    else:
        context.scene.cycles.device = 'CPU'
    
    # Enable GPU compute
    if context.scene.cycles.device == 'GPU':
        context.scene.cycles.use_gpu = True 