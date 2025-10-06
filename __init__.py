import bpy

# first thing it should do is import everything in the libs folder before doing anything else
from . import lib_loader
lib_loader.import_libs()

# only then it can import external libraries
from .utils import qr_utils, mesh_utils, material_utils


class MESH_OT_add_custom_mesh(bpy.types.Operator):
    """Add a Custom Mesh"""
    bl_idname = "mesh.add_custom_mesh"
    bl_label = "Add Custom Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    # User input fields (appear in popup)
    data: bpy.props.StringProperty(
        name="Data",
        default="https://github.com/inkihong9",
        description="Data to encode for creating QR code"
    )

    # this function is called when OK is clicked in the popup modal
    def execute(self, context):
        # step 1. get user input
        input_data = self.data

        # step 2. get QR code matrix from user input
        qr_matrix = qr_utils.get_qr_matrix(input_data)

        # step 3. create stone for duplicating throughout the QR code matrix
        mesh_utils.create_stone()

        # step 4. create 2 materials: black and white
        white_mat = material_utils.create_material("ivory-white", (1, 0.939, 0.584, 1))
        black_mat = material_utils.create_material("jet-black", (0.002, 0.000607, 0.000911, 1))

        # step n. duplicate stone based on the QR code matrix
        
        # Example: create a circle mesh with user inputs
        # bpy.ops.mesh.primitive_circle_add(
        #     radius=1,
        #     vertices=10,
        #     enter_editmode=False,
        #     align='WORLD',
        #     location=(0, 0, 0)
        # )
        
        return {'FINISHED'}

    # this function is called when the operator (Add > Mesh > Custom Mesh) is clicked
    def invoke(self, context, event):
        # This makes the popup appear before execution
        return context.window_manager.invoke_props_dialog(self)


# Register in the Add > Mesh menu
def menu_func(self, context):
    self.layout.operator(MESH_OT_add_custom_mesh.bl_idname,
                         text="Custom Mesh")

# this function is called when the add-on is enabled in Edit > Preferences > Add-ons
def register():
    bpy.utils.register_class(MESH_OT_add_custom_mesh)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

# this function is called when the add-on is disabled in Edit > Preferences > Add-ons
def unregister():
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(MESH_OT_add_custom_mesh)


if __name__ == "__main__":
    register()
