import bpy

from .utils import (
    setup_bake_settings,
    prepare_material_for_baking,
    create_or_get_image,
    save_baked_image,
    setup_render_engine
)

class BAKE_OT_bake_texture(bpy.types.Operator):
    """Bake texture for the active object"""
    bl_idname = "bake.bake_texture"
    bl_label = "Bake Texture"
    bl_description = "Bake texture for the active object"
    bl_options = {'REGISTER', 'UNDO'}

    _timer = None
    _baking = False
    _image = None
    _current_engine = None

    def modal(self, context, event):
        if event.type == 'TIMER':
            if self._baking:
                # Update progress
                if context.scene.render.bake.use_selected_to_active:
                    progress = context.scene.render.bake.progress
                else:
                    progress = context.scene.render.bake.progress
                
                # Check if baking is complete
                if progress >= 1.0:
                    self._baking = False
                    # Save the image
                    success, filepath = save_baked_image(
                        self._image,
                        context.scene.bake_save_path,
                        context.active_object.name,
                        context.scene.bake_type
                    )
                    if success:
                        self.report({'INFO'}, f"Bake completed and saved to: {filepath}")
                    else:
                        self.report({'ERROR'}, "Failed to save baked image")
                    
                    # Restore original render engine
                    context.scene.render.engine = self._current_engine
                    return {'FINISHED'}
                
                # Update progress bar
                context.workspace.status_text_set(f"Baking: {progress*100:.1f}%")
            
        return {'PASS_THROUGH'}

    def execute(self, context):
        # Get active object
        obj = context.active_object
        if not obj:
            self.report({'ERROR'}, "No active object")
            return {'CANCELLED'}
        
        # Get active material
        if not obj.active_material:
            self.report({'ERROR'}, "No active material")
            return {'CANCELLED'}
        
        mat = obj.active_material
        
        try:
            # Store original render engine
            self._current_engine = setup_render_engine(context)
            
            # Create or get image for baking
            self._image = create_or_get_image(
                obj.name,
                context.scene.bake_type,
                context.scene.bake_resolution
            )
            
            # Prepare material for baking
            image_node = prepare_material_for_baking(mat)
            image_node.image = self._image
            
            # Set up bake settings
            setup_bake_settings(context, context.scene.bake_type)
            
            # Start baking
            self._baking = True
            context.scene.render.bake.use_selected_to_active = False
            
            # Add timer for progress updates
            wm = context.window_manager
            self._timer = wm.event_timer_add(0.1, window=context.window)
            wm.modal_handler_add(self)
            
            return {'RUNNING_MODAL'}
            
        except Exception as e:
            self.report({'ERROR'}, f"Baking failed: {str(e)}")
            # Restore original render engine
            if self._current_engine:
                context.scene.render.engine = self._current_engine
            return {'CANCELLED'}

    def cancel(self, context):
        if self._timer:
            context.window_manager.event_timer_remove(self._timer)
        if self._current_engine:
            context.scene.render.engine = self._current_engine
