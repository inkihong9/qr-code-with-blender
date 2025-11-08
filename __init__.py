import bpy

# first thing it should do is import everything in the libs folder before doing anything else
from . import lib_loader
lib_loader.import_libs()

# only then it can import external libraries
from .utils import qr_utils, mesh_utils, collection_utils
from . import global_vars as gv


# global reference for the active popup operator
_popup_ref = None


# Each input URL in the dynamic input list
class InputUrl(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty(
        name="URL", 
        default="", 
        description="Input URL for QR code generation"
    )


class MESH_OT_add_custom_mesh(bpy.types.Operator):
    """Add a Custom Mesh"""
    bl_idname = "mesh.add_custom_mesh"
    bl_label = "Add Custom Mesh"
    bl_options = {'REGISTER', 'UNDO'}

    # User input fields (appear in popup)
    time_interval: bpy.props.IntProperty(**gv.time_interval_input_params)
    flip_time: bpy.props.IntProperty(**gv.flip_time_input_params)
    urls: bpy.props.CollectionProperty(type=InputUrl)


    def draw(self, context):
        layout = self.layout

        layout.prop(self, "time_interval")
        layout.prop(self, "flip_time")

        layout.label(text="URLs:")
        for i, item in enumerate(self.urls):
            row = layout.row(align=True)
            row.prop(item, "value", text=f"URL {i+1}")
            op = row.operator("myaddon.remove_item_in_popup", text="", icon="X")
            op.index = i

        layout.operator("myaddon.add_item_in_popup", text="Add URL", icon="ADD").operator_id = self.bl_idname


    # this function is called when OK is clicked in the popup modal
    def execute(self, context):
        # step 1. initialize and get user input
        qr_matrices = []
        gv.saved_time_interval = self.time_interval
        gv.saved_flip_time = self.flip_time
        input_urls = [item.value for item in self.urls]

        # step 1.5. set the frame back to 1
        bpy.context.scene.frame_set(1)
        
        # TODO: step 2. do the validations on the input urls, create a separate user story for this later
        if input_urls == [''] or len(input_urls) == 0:
            self.report({'ERROR'}, "At least one URL must be provided.")
            return {'CANCELLED'}

        # step 3. get QR code matrix from user input
        for url in input_urls:
            qr_matrix = qr_utils.get_qr_matrix(url)
            qr_matrices.append(qr_matrix)
            print(f"url = {url}")
            print(f"total length of QR code modules = {len(qr_matrix)}")

        # step 4. create a new collection for storing QR code mesh
        collection_utils.create_qr_code_collection()

        # step 5. create stone for duplicating throughout the QR code matrix
        gv.stone = mesh_utils.create_stone_v2("stone", (1,1,0.3), (-1,1,0))

        # step 6. build the QR code base - all stones are switched ON
        mesh_utils.build_qr_code_base()

        # step 7. build the QR code by flipping stones based on the QR code matrices
        for qr_matrix in qr_matrices:
            mesh_utils.build_qr_code_v3(qr_matrix)

        # step 8. hide the original stone from view
        gv.stone.hide_set(True)
        gv.stone.hide_render = True

        # TODO: DEPRECATED step 5. create stone for duplicating throughout the QR code matrix
        # future plan: allow the user to choose stone size, shape, scale, how materials are assigned, etc.
        # gv.white_stone = mesh_utils.create_stone("white-stone", (1,1,0.3), (-1,1,0))
        # gv.black_stone = mesh_utils.create_stone("black-stone", (1,1,0.3), (-1,1.2,0))

        # TODO: DEPRECATED step 6. create 2 materials: black and white
        # future plan: allow user to choose colors in the popup if possible, white will be limited choices, but non-white color
        #              will be a myriad of colors for high contrast
        # white_mat = material_utils.create_material("ivory-white", (1, 0.939, 0.584, 1))
        # black_mat = material_utils.create_material("jet-black", (0.002, 0.000607, 0.000911, 1))

        # TODO: DEPRECATED step 6. assign materials to stones
        # gv.white_stone.data.materials.clear()
        # gv.white_stone.data.materials.append(white_mat)
        # gv.black_stone.data.materials.clear()
        # gv.black_stone.data.materials.append(black_mat)

        # TODO: DEPRECATED step 7. build QR code by duplicating the white and black stones based on the QR code matrix
        # mesh_utils.build_qr_code(qr_matrix)
        # mesh_utils.build_qr_code_v2(qr_matrix)

        # # step 8. hide the original stones from view
        # gv.white_stone.hide_set(True)
        # gv.white_stone.hide_render = True
        # gv.black_stone.hide_set(True)
        # gv.black_stone.hide_render = True

        # step 9. apparently this return value is needed
        return {'FINISHED'}
    

    # this function is called when the operator (Add > Mesh > QR Code) is clicked
    def invoke(self, context, event):
        global _popup_ref
        _popup_ref = self  # store reference globally

        # Ensure at least one input exists to start
        if not len(self.urls):
            self.urls.add()

        # This makes the popup appear before execution
        return context.window_manager.invoke_props_dialog(self)


# Register in the Add > Mesh menu
def menu_func(self, context):
    self.layout.operator(MESH_OT_add_custom_mesh.bl_idname,
                         text="QR Code")
    

class MYADDON_OT_add_item_in_popup(bpy.types.Operator):
    bl_idname = "myaddon.add_item_in_popup"
    bl_label = "Add Item in Popup"

    operator_id: bpy.props.StringProperty()

    def execute(self, context):
        # Find the running operator instance
        global _popup_ref
        op = _popup_ref
        if op and op.bl_idname == self.operator_id:
            op.urls.add()
        return {'FINISHED'}


class MYADDON_OT_remove_item_in_popup(bpy.types.Operator):
    bl_idname = "myaddon.remove_item_in_popup"
    bl_label = "Remove Item in Popup"

    index: bpy.props.IntProperty()

    def execute(self, context):
        # Find the running operator instance
        global _popup_ref
        op = _popup_ref
        if op and 0 <= self.index < len(op.urls):
            op.urls.remove(self.index)
        return {'FINISHED'}
    

# Registration
classes = (
    InputUrl,
    MYADDON_OT_add_item_in_popup,
    MYADDON_OT_remove_item_in_popup,
)


# this function is called when the add-on is enabled in Edit > Preferences > Add-ons
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.urls = bpy.props.CollectionProperty(type=InputUrl)
    bpy.utils.register_class(MESH_OT_add_custom_mesh)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)
    

# this function is called when the add-on is disabled in Edit > Preferences > Add-ons
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.urls
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)
    bpy.utils.unregister_class(MESH_OT_add_custom_mesh)


if __name__ == "__main__":
    register()
