import bpy

# Create black material
black_mat = bpy.data.materials.new(name="Black_Material")
black_mat.use_nodes = True
nodes = black_mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (0, 0, 0, 1)  # Black (R,G,B,A)

# Create white material
white_mat = bpy.data.materials.new(name="White_Material")
white_mat.use_nodes = True
nodes = white_mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (1, 1, 1, 1)  # White (R,G,B,A)

print("Created materials: Black_Material and White_Material")
