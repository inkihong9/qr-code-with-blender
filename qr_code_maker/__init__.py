import bpy

class MESH_OT_add_custom_mesh(bpy.types.Operator):
    """Add a Custom Mesh"""
    bl_idname = "mesh.add_custom_mesh"
    bl_label = "Add Custom Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    # User input fields (appear in popup)
    size: bpy.props.FloatProperty(
        name="Size",
        default=1.0,
        min=0.1,
        max=10.0,
        description="Size of the mesh"
    )
    segments: bpy.props.IntProperty(
        name="Segments",
        default=16,
        min=3,
        max=128,
        description="Number of segments"
    )

    def execute(self, context):
        # Example: create a circle mesh with user inputs
        bpy.ops.mesh.primitive_circle_add(
            radius=self.size,
            vertices=self.segments,
            enter_editmode=False,
            align='WORLD',
            location=(0, 0, 0)
        )
        return {'FINISHED'}

    def invoke(self, context, event):
        # This makes the popup appear before execution
        return context.window_manager.invoke_props_dialog(self)


# Register in the Add > Mesh menu
def menu_func(self, context):
    self.layout.operator(MESH_OT_add_custom_mesh.bl_idname,
                         text="Custom Mesh")


def register():
    bpy.utils.register_class(MESH_OT_add_custom_mesh)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(MESH_OT_add_custom_mesh)


if __name__ == "__main__":
    register()
