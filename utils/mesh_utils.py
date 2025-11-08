import bpy, bmesh, math
from .. import global_vars as gv
from . import material_utils


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
    white_mat = material_utils.create_material("ivory-white", gv.ivory_white_rgba)
    black_mat = material_utils.create_material("jet-black", gv.jet_black_rgba)
    

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

    return stone


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


'''
Builds a non-working N x N QR code by duplicating the original stone
by a correct number of stones in x and y direction
'''
def build_qr_code_base():
    curr_y = 0
    curr_x = 0
    n = gv.qr_matrix_size
    N = n + (gv.border * 2)
    m = (n // 3) + (1 if (n // 3) % 2 == 0 else 0)
    i_start = ((N - m) // 2)
    i_end = i_start + m

    # iterate through 0 to gv.qr_matrix_size in y direction
    for i in range(0, N):
        
        # iterate through 0 to gv.qr_matrix_size in x direction
        for j in range(0, N):
            
            # duplicate the original stone
            stone_copy = gv.stone.copy()
            stone_copy.data = gv.stone.data.copy()
            # set the location of the duplicated stone
            stone_copy.location = (j * 0.1, -i * 0.1, 0)
            # move the stone to the "qr-code" collection
            gv.qr_code_coll.objects.link(stone_copy)

            # increment x by 0.1 for the next stone
            curr_x += 0.1

            # write the stone object's name into the global qr_matrix_stone_names
            gv.qr_matrix_stone_names[i][j] = stone_copy.name

            # insert the initial keyframe
            stone_copy.keyframe_insert(data_path="rotation_euler", index=-1)

            if i_start <= i < i_end and i_start <= j < i_end:
                # hide the current stone to create empty center
                stone_copy.hide_set(True)
                stone_copy.hide_render = True

        # at the end of each row, decrement y by 0.1 and reset x to 0
        curr_y -= 0.1
        curr_x = 0


'''
Iterate through the QR code matrix and build the QR code by duplicating the stone. 
For each bit, if it's in the center area, skip duplicating the stone to create empty center.
Duplicate the stone regardless of the bit value, but if the bit is ON, leave it as is, 
so it displays black. Else if the bit is OFF, flip it so it displays white.
'''
def build_qr_code_v3(qr_matrix):
    n = gv.qr_matrix_size
    N = n + (gv.border * 2)
    flip_time_keyframe = bpy.context.scene.frame_current + gv.saved_flip_time
    time_interval_keyframe = flip_time_keyframe + gv.saved_time_interval

    # Deselect all first
    bpy.ops.object.select_all(action='DESELECT')

    # iterate through 0 to gv.qr_matrix_size in y direction
    for i in range(0, N):
        
        # iterate through 0 to gv.qr_matrix_size in x direction
        for j in range(0, N):

            prev_bit = gv.qr_matrix_prev_state[i][j]
            curr_bit = qr_matrix[i][j]
            stone_name = gv.qr_matrix_stone_names[i][j]
            stone_obj = bpy.data.objects.get(stone_name)

            if stone_obj:
                # Select and make it active
                stone_obj.select_set(True)
                bpy.context.view_layer.objects.active = stone_obj

                # set the frame
                bpy.context.scene.frame_set(flip_time_keyframe)

                if prev_bit != curr_bit:
                    # Rotate by 180 degrees on X axis (in radians)
                    stone_obj.rotation_euler[0] += math.pi
                else:
                    # Reset rotation to 360
                    stone_obj.rotation_euler[0] += (math.pi*2)

                # Insert keyframe for rotation at frame N
                stone_obj.keyframe_insert(data_path="rotation_euler", index=-1)

                # set the frame for time interval
                bpy.context.scene.frame_set(time_interval_keyframe)

                # Insert another keyframe
                stone_obj.keyframe_insert(data_path="rotation_euler", index=-1)

                # Deselect the object
                stone_obj.select_set(False)
                bpy.context.view_layer.objects.active = None
            else:
                print("Error: Stone object not found:", stone_name)

    gv.qr_matrix_prev_state = qr_matrix
