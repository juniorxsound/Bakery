import bpy

class BAKE_PT_main_panel(bpy.types.Panel):
    bl_label = "Bakery"
    bl_idname = "BAKE_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Bakery'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.mode in {'OBJECT', 'EDIT_MESH'}

    def draw(self, context):
        print("Drawing Bake Tools panel...")  # Debug print
        layout = self.layout
        
        # Object Selection Box
        box = layout.box()
        box.label(text="Object Selection")
        row = box.row()
        row.label(text="Active Object: " + (context.active_object.name if context.active_object else "None"))
        print("Drew object selection box")  # Debug print
        
        # Bake Settings Box
        box = layout.box()
        box.label(text="Bake Settings")
        print("Drew bake settings box")  # Debug print
        
        # Bake Type Selection
        col = box.column(align=True)
        col.label(text="Bake Type:")
        col.prop(context.scene, "bake_type", text="")
        print("Drew bake type")  # Debug print
        
        # Resolution Selection
        col = box.column(align=True)
        col.label(text="Resolution:")
        col.prop(context.scene, "bake_resolution", text="")
        print("Drew resolution")  # Debug print
        
        # Save Path
        col = box.column(align=True)
        col.label(text="Save Path:")
        col.prop(context.scene, "bake_save_path", text="")
        print("Drew save path")  # Debug print
        
        # Bake Button
        row = layout.row()
        row.operator("bake.bake_texture", text="Bake Texture", icon='RENDER_STILL')
        print("Drew bake button")  # Debug print
        
        # Help Box
        box = layout.box()
        box.label(text="Instructions:")
        col = box.column()
        col.label(text="1. Select an object with a material")
        col.label(text="2. Choose bake type and resolution")
        col.label(text="3. Set save path")
        col.label(text="4. Click Bake Texture")
        print("Drew help box") 