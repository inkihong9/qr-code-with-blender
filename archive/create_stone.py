import bpy
import bmesh

# NOTE: all measurements in meters
# output: a stone mesh with top half jet black and bottom half ivory white

'''
step 1. create a stone mesh with these properties:
- radius = 0.05m
- coordinate = (-1m, 1m, 0m)
- name = stone
- scale z-axis by 30%
'''
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(-1,1,0))
stone = bpy.context.active_object
stone.name = "stone"
stone.scale = (1,1,0.3)


'''
step 2. create 2 materials
- jet black (R:54, G:69, B:79)
- ivory white (R:242, G:239, B:222)
'''
black_mat = bpy.data.materials.new(name="jet-black")
black_mat.use_nodes = True
nodes = black_mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (0.002, 0.000607, 0.000911, 1)

white_mat = bpy.data.materials.new(name="ivory-white")
white_mat.use_nodes = True
nodes = white_mat.node_tree.nodes
bsdf = nodes.get("Principled BSDF")
if bsdf:
    bsdf.inputs["Base Color"].default_value = (1, 0.939, 0.584, 1)


'''
step 3. assign materials to stone
'''
stone.data.materials.clear()
stone.data.materials.append(white_mat)
stone.data.materials.append(black_mat)

'''
step 4. color the stone
- top half = jet black
- bottom half = ivory white
'''

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

# Assign white material (slot 1) to selected faces
stone.active_material_index = 1
bpy.ops.object.material_slot_assign()

# Update mesh and return to object mode
bmesh.update_edit_mesh(stone.data, loop_triangles=False, destructive=False)
bpy.ops.object.mode_set(mode='OBJECT')
