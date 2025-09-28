import bpy
import bmesh

'''
1. create a UV sphere with radius of 5cm at location x = -1m, y = 1m, z = 0m
2. name it stone
3. scale it by 30% in z-axis
'''
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(-1,1,0))
stone = bpy.context.active_object
stone.name = "stone"
stone.scale = (1,1,0.3)





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

stone.data.materials.clear()




stone.data.materials.append(white_mat)

stone.data.materials.append(black_mat)







# Switch to Edit Mode
bpy.context.view_layer.objects.active = stone
bpy.ops.object.mode_set(mode='EDIT')


# Access the mesh in edit mode
mesh = bmesh.from_edit_mesh(stone.data)

# Deselect everything first
for f in mesh.faces:
    f.select = False

# Select faces where average Z > 0
for f in mesh.faces:
    avg_z = sum(v.co.z for v in f.verts) / len(f.verts)
    if avg_z > 0:
        f.select = True

# Update the selection in viewport
bmesh.update_edit_mesh(stone.data, loop_triangles=False, destructive=False)

print("Selected all faces in 'stone' with Z > 0")

# Assign white material (slot 1) to selected faces
stone.active_material_index = 1
bpy.ops.object.material_slot_assign()

# Update mesh and return to object mode
bmesh.update_edit_mesh(stone.data, loop_triangles=False, destructive=False)
bpy.ops.object.mode_set(mode='OBJECT')


'''




# Select top half (Z >= 0)
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.mesh.select_all(action='SELECT')  # temporarily select all
bpy.ops.mesh.region_to_loop()  # makes sure boundary is clean (optional)
bpy.ops.mesh.select_all(action='DESELECT')

bpy.ops.mesh.select_all(action='SELECT')  # select everything first
bpy.ops.mesh.bisect(
    plane_co=(0, 0, 0),
    plane_no=(0, 0, 1),
    clear_inner=False,
    clear_outer=False
)

# Assign selected (top half) to black material
bpy.ops.object.material_slot_set(assign=True)

# Switch back to Object Mode
bpy.ops.object.mode_set(mode='OBJECT')

# Now assign bottom half to white
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.bisect(
    plane_co=(0, 0, 0),
    plane_no=(0, 0, -1),
    clear_inner=False,
    clear_outer=False
)
stone.active_material_index = 1  # White material slot
bpy.ops.object.material_slot_set(assign=True)

# Switch back to Object Mode
bpy.ops.object.mode_set(mode='OBJECT')


# 2. Create a real duplicate with its own mesh data
stone_copy = stone.copy()
stone_copy.data = stone.data.copy()
stone_copy.name = "stone_copy"
stone_copy.location = (3, 0, 0)

# Link the duplicate to the current collection
bpy.context.collection.objects.link(stone_copy)
'''