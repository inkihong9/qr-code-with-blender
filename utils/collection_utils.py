import bpy
from .. import global_vars as gv


# create a single collection and name it "qr-code"
def create_qr_code_collection():
    # Define the name of your new collection
    qr_code_coll_name = "qr-code"

    # Check if the collection already exists
    if qr_code_coll_name not in bpy.data.collections:
        # Create a new collection
        new_collection = bpy.data.collections.new(qr_code_coll_name)
        
        # Link the new collection to the Scene Collection
        bpy.context.scene.collection.children.link(new_collection)
        
        # Store the collection in global_vars
        gv.qr_code_coll = new_collection
