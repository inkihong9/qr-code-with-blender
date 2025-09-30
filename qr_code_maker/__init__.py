import bpy


class OBJECT_OT_add_custom_cube(bpy.types.Operator):
    bl_idname = "mesh.add_custom_cube"
    bl_label = "okay im gonna reload the script from blender"
    bl_description = "okay lets try this again..."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add()
        self.report({'INFO'}, "Custom Cube added!")
        return {'FINISHED'}


# Menu function that tells Blender where to put our operator
def add_custom_menu(self, context):
    self.layout.operator(
        OBJECT_OT_add_custom_cube.bl_idname,
        text=OBJECT_OT_add_custom_cube.bl_label,
        icon='MESH_CUBE'
    )


def register():
    bpy.utils.register_class(OBJECT_OT_add_custom_cube)
    # Append our operator into the "Add Mesh" menu (Shift + A → Mesh → …)
    bpy.types.VIEW3D_MT_mesh_add.append(add_custom_menu)


def unregister():
    # Clean up on unregister
    bpy.types.VIEW3D_MT_mesh_add.remove(add_custom_menu)
    bpy.utils.unregister_class(OBJECT_OT_add_custom_cube)
