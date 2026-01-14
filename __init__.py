import bpy 

# first thing it should do is import everything in the libs folder before doing anything else
from . import lib_loader
lib_loader.import_libs()

# only then it can import external libraries
from .utils import qr_utils, mesh_utils, collection_utils
from . import global_vars as gv

# time module for time elapsed
import time


# global reference for the active popup operator
_popup_ref = None


# Each input URL in the dynamic input list
class InputUrl(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty(
        name="URL", 
        default="https://www.github.com/inkihong9", 
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
        # capture start time
        start_time = round(time.time())

        # step 1. initialize and get user input
        qr_matrices = []
        gv.saved_time_interval = self.time_interval
        gv.saved_flip_time = self.flip_time
        input_urls = [item.value for item in self.urls]

        # step 2. force set the active frame back to 1
        bpy.context.scene.frame_set(1)
        
        # TODO: step 3. do the validations on the input urls, create a separate user story for this later
        if input_urls == [''] or len(input_urls) == 0:
            self.report({'ERROR'}, "At least one URL must be provided.")
            return {'CANCELLED'}
        
        # step 4. grab the longest url by length
        longest = max(input_urls, key=len)

        # step 5. get a qr code matrix and qr code version of the longest url
        ver, qr_len, matrix = qr_utils.get_qr_matrix(longest)

        # step 6. get QR code matrix from user input
        for url in input_urls:
            version, qr_length, qr_matrix = qr_utils.get_qr_matrix(data=url, ver=ver)
            qr_matrices.append(qr_matrix)
            print(f"url = {url}")
            print(f"total length of QR code modules = {len(qr_matrix)}")

        # step 7. create a new collection for storing QR code mesh
        collection_utils.create_qr_code_collection()

        # step 8. create stone for duplicating throughout the QR code matrix
        gv.stone = mesh_utils.create_stone_v2("stone", (1,1,0.3), (-1,1,0))

        # step 9. build initial QR code
        mesh_utils.build_initial_qr_code(qr_matrix=qr_matrices[0])

        # step 10. insert keyframe for all stones in the QR code in bulk
        for obj in bpy.data.collections['qr-code'].all_objects:
            obj.keyframe_insert(data_path="rotation_euler", index=-1)

        # step 11. build the QR code by flipping stones based on the QR code matrices
        for qr_matrix in qr_matrices[1:]:

            # step 11a. set the next frame numbers to insert the keyframes at, and transform the QR codes
            flip_time_keyframe = bpy.context.scene.frame_current + gv.saved_flip_time
            time_interval_keyframe =  flip_time_keyframe + gv.saved_time_interval
            
            bpy.context.scene.frame_set(flip_time_keyframe)
            mesh_utils.build_qr_code(qr_matrix)

            # step 11b. insert keyframe
            for obj in bpy.data.collections['qr-code'].all_objects:
                obj.keyframe_insert(data_path="rotation_euler", index=-1)

            # step 11c. set the frame for time interval
            bpy.context.scene.frame_set(time_interval_keyframe)

            # step 11d. Insert another keyframe
            for obj in bpy.data.collections['qr-code'].all_objects:
                obj.keyframe_insert(data_path="rotation_euler", index=-1)

        # step 12. hide the original stone from view
        gv.stone.hide_set(True)
        gv.stone.hide_render = True

        # capture end time
        end_time = round(time.time())

        # print both start and end time values
        print(f"start = {start_time}, end = {end_time}")
        print(f"time elapsed = {end_time - start_time} seconds")

        # step 13. apparently this return value is needed
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
