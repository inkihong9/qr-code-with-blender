import bpy

# first thing it should do is import everything in the libs folder before doing anything else
from . import lib_loader
lib_loader.import_libs()

# only then it can import external libraries
from .utils import qr_utils, mesh_utils, material_utils, collection_utils
from . import global_vars as gv

# TODO: remove qr_code_ver_utils import when finished with SPIKE user story 
#       (i'm offline now, can't remember which one)
# temporarily import qr_code_ver_utils
from .utils import qr_code_ver_utils


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

        # TODO: remove print_qr_code_version_sizes function call when finished with SPIKE user story 
        #       (i'm offline now, can't remember which one)
        # temporarily start off with printing the QR code version sizes
        qr_code_ver_utils.print_qr_code_version_sizes()
        lcm = qr_code_ver_utils.get_lcm([21,25,29,33,37,41,45,49,53,57,61,65,69,73,77,81,85,89,93,97,101,105,109,113,117,121,125,129,133,137,141,145,149,153,157,161,165,169,173,177])
        print(f"LCM of all QR code version sizes: {lcm}")

        # step 1. get user input
        input_data = self.data

        # step 2. get QR code matrix from user input
        qr_matrix = qr_utils.get_qr_matrix(input_data)

        # step 3. create a new collection for storing QR code mesh
        collection_utils.create_qr_code_collection()

        # step 3. create stone for duplicating throughout the QR code matrix
        # future plan: allow the user to choose stone size, shape, scale, how materials are assigned, etc.
        gv.white_stone = mesh_utils.create_stone("white-stone", (1,1,0.3), (-1,1,0))
        gv.black_stone = mesh_utils.create_stone("black-stone", (1,1,0.3), (-1,1.2,0))

        # step 4. create 2 materials: black and white
        # future plan: allow user to choose colors in the popup if possible, white will be limited choices, but non-white color
        #              will be a myriad of colors for high contrast
        white_mat = material_utils.create_material("ivory-white", (1, 0.939, 0.584, 1))
        black_mat = material_utils.create_material("jet-black", (0.002, 0.000607, 0.000911, 1))

        # step 5. assign materials to stones
        gv.white_stone.data.materials.clear()
        gv.white_stone.data.materials.append(white_mat)
        gv.black_stone.data.materials.clear()
        gv.black_stone.data.materials.append(black_mat)

        # step 6. build QR code by duplicating the white and black stones based on the QR code matrix
        # mesh_utils.build_qr_code(qr_matrix)
        mesh_utils.build_qr_code_v2(qr_matrix)

        # step 7. hide the original stones from view
        gv.white_stone.hide_set(True)
        gv.white_stone.hide_render = True
        gv.black_stone.hide_set(True)
        gv.black_stone.hide_render = True

        # step 8. apparently this return value is needed
        return {'FINISHED'}

    # this function is called when the operator (Add > Mesh > QR Code) is clicked
    def invoke(self, context, event):
        # This makes the popup appear before execution
        return context.window_manager.invoke_props_dialog(self)


# Register in the Add > Mesh menu
def menu_func(self, context):
    self.layout.operator(MESH_OT_add_custom_mesh.bl_idname,
                         text="QR Code")

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
