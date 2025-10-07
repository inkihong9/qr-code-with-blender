import bpy

'''
create a single collection and name it "qr-code"
'''
def create_qr_code_collection():
    # Define the name of your new collection
    qr_code_coll_name = "qr-code"

    # Check if the collection already exists
    if qr_code_coll_name not in bpy.data.collections:
        # Create a new collection
        new_collection = bpy.data.collections.new(qr_code_coll_name)
        
        # Link the new collection to the Scene Collection
        bpy.context.scene.collection.children.link(new_collection)
        
        print(f"Collection '{qr_code_coll_name}' created and linked to Scene Collection.")
    else:
        print(f"Collection '{qr_code_coll_name}' already exists.")
