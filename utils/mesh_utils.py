import bpy, bmesh
from .. import global_vars as gv
from . import material_utils


'''
create a single stone and return the object
location param is a tuple of (x, y, z) coordinates
'''
def create_stone(name:str, scale:tuple, location:tuple):
    # create a new stone
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=location)
    stone = bpy.context.active_object
    stone.name = name
    stone.scale = scale

    # move the stone to the "qr-code" collection
    gv.qr_code_coll.objects.link(stone)

    # remove the stone from the default collection
    bpy.context.collection.objects.unlink(stone)
 
    return stone


'''
create a single stone and return the object
location param is a tuple of (x, y, z) coordinates
'''
def create_stone_v2(name:str, scale:tuple, location:tuple):
    '''
    step 1. create a stone mesh with these properties:
    - radius = 0.05m
    - coordinate = (-1m, 1m, 0m)
    - name = stone
    - scale z-axis by 30%
    '''
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=location)
    stone = bpy.context.active_object
    stone.name = name
    stone.scale = scale


    '''
    step 2. create 2 materials
    - jet black (R:54, G:69, B:79)
    - ivory white (R:242, G:239, B:222)
    '''
    white_mat = material_utils.create_material("ivory-white", (1, 0.939, 0.584, 1))
    black_mat = material_utils.create_material("jet-black", (0.002, 0.000607, 0.000911, 1))
    # black_mat = bpy.data.materials.new(name="jet-black")
    # black_mat.use_nodes = True
    # nodes = black_mat.node_tree.nodes
    # bsdf = nodes.get("Principled BSDF")
    # if bsdf:
    #     bsdf.inputs["Base Color"].default_value = (0.002, 0.000607, 0.000911, 1)

    # white_mat = bpy.data.materials.new(name="ivory-white")
    # white_mat.use_nodes = True
    # nodes = white_mat.node_tree.nodes
    # bsdf = nodes.get("Principled BSDF")
    # if bsdf:
    #     bsdf.inputs["Base Color"].default_value = (1, 0.939, 0.584, 1)


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



'''
iterate through the QR code matrix and build the QR code by duplicating 
the correct stone (black or white) at the correct location
qr_matrix param is a 2D list of booleans representing the QR code
'''
def build_qr_code(qr_matrix):
    curr_y = 0
    curr_x = 0

    # iterate through a row of bits
    for row_of_bits in qr_matrix:

        # iterate through each bit in the row
        for bit in row_of_bits:

            # initialize a variable to hold the duplicated stone for each bit
            stone_copy = None

            # each bit is 0 or 1 (or T/F), if 1 (T), duplicate black stone, else (F) duplicate white stone
            if bit:
                stone_copy = gv.black_stone.copy()
                stone_copy.data = gv.black_stone.data.copy()
            else:
                stone_copy = gv.white_stone.copy()
                stone_copy.data = gv.white_stone.data.copy()

            # set the location of the duplicated stone
            stone_copy.location = (curr_x, curr_y, 0)

            # move the stone to the "qr-code" collection
            gv.qr_code_coll.objects.link(stone_copy)

            # increment x by 0.1 for the next stone
            curr_x += 0.1

        # at the end of each row, decrement y by 0.1 and reset x to 0
        curr_y -= 0.1
        curr_x = 0


'''
iterate through the QR code matrix and build the QR code by duplicating 
the correct stone (black or white) at the correct location
qr_matrix param is a 2D list of booleans representing the QR code
this also creates an empty space in the center of the QR code for putting logo in it
'''
def build_qr_code_v2(qr_matrix):
    curr_y = 0
    curr_x = 0

    N = len(qr_matrix)
    n = N - (gv.border * 2)

    m = (n // 3) + (1 if (n // 3) % 2 == 0 else 0)
    i_start = ((N - m) // 2)
    i_end = i_start + m

    # 0 to 28 total = 29
    # to determine start and end index for empty center
    # i = ((N - m) / 2) - 1
    #   = ((29 - 9) / 2) - 1
    #   = (20 / 2) - 1
    #   = 10 - 1
    #   = 9
    # j = i + m
    #   = 9 + 9
    #   = 18

    '''
    IH (2025-10-13): version 2 algorithm for building QR code with empty center
    need to compute: 
    N - size of QR matrix (with border): N = len(qr_matrix)
    n - size of QR matrix (without border): n = N - (gv.border * 2)
      - length of QR matrix (n) for all versions of QR code
    m - size of empty center (without border): m = not sure yet, but should be an odd number
      - maybe floor(m/3), add 1 if even to make it odd
      - need to experiment
    i - start index for empty center
    j - end index for empty center
    1. determine the size of the qr_matrix (n x n) - 
    2. calculate m as follows: m = ?? need to figure out the formula for this
    '''

    # iterate through a row of bits
    for i, row_of_bits in enumerate(qr_matrix):

        # iterate through each bit in the row
        for j, bit in enumerate(row_of_bits):

            # initialize a variable to hold the duplicated stone for each bit
            stone_copy = None

            # each bit is 0 or 1 (or T/F), if 1 (T), duplicate black stone, else (F) duplicate white stone
            if bit:
                stone_copy = gv.black_stone.copy()
                stone_copy.data = gv.black_stone.data.copy()
            else:
                stone_copy = gv.white_stone.copy()
                stone_copy.data = gv.white_stone.data.copy()

            # set the location of the duplicated stone
            stone_copy.location = (curr_x, curr_y, 0)

            # move the stone to the "qr-code" collection
            gv.qr_code_coll.objects.link(stone_copy)

            # increment x by 0.1 for the next stone
            curr_x += 0.1

            if i_start <= i < i_end and i_start <= j < i_end:
                # hide the current stone to create empty center
                stone_copy.hide_set(True)
                stone_copy.hide_render = True

        # at the end of each row, decrement y by 0.1 and reset x to 0
        curr_y -= 0.1
        curr_x = 0
