import bpy
import os
import sys
from . import test_me
# , cleanup_scene, create_icosphere_meshes, create_materials, create_stone, make_qr_code_matrix


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
    '''
    this will add all packages in the "libs" folder to sys.path
    so i can use external packages like qrcode
    '''
    # Path to the "libs" folder inside the extension
    addon_dir = os.path.dirname(__file__)
    libs_dir = os.path.join(addon_dir, "libs")

    # Add to sys.path if not already there
    if libs_dir not in sys.path:
        sys.path.append(libs_dir)

    # Call the test function to see if it works
    test_me.test_function()
    
    # Register our operator    
    bpy.utils.register_class(OBJECT_OT_add_custom_cube)
    # Append our operator into the "Add Mesh" menu (Shift + A → Mesh → …)
    bpy.types.VIEW3D_MT_mesh_add.append(add_custom_menu)


def unregister():
    # Clean up on unregister
    bpy.types.VIEW3D_MT_mesh_add.remove(add_custom_menu)
    bpy.utils.unregister_class(OBJECT_OT_add_custom_cube)
