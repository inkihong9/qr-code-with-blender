import bpy, bmesh, math
from .. import global_vars as gv
from . import material_utils


'''
create a single module and return the object
location param is a tuple of (x, y, z) coordinates
'''
def create_module(name:str, scale:tuple, location:tuple):
    '''
    step 1. create a module mesh with these properties:
    - radius = 0.05m
    - coordinate = (-1m, 1m, 0m)
    - name = module
    - scale z-axis by 30%
    '''
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=location)
    module = bpy.context.active_object
    module.name = name
    module.scale = scale


    '''
    step 2. create 2 materials
    - jet black (R:54, G:69, B:79)
    - ivory white (R:242, G:239, B:222)
    '''
    white_mat = material_utils.create_material("ivory-white", gv.ivory_white_rgba)
    black_mat = material_utils.create_material("jet-black", gv.jet_black_rgba)
    

    '''
    step 3. assign materials to module
    '''
    module.data.materials.clear()
    module.data.materials.append(white_mat)
    module.data.materials.append(black_mat)

    '''
    step 4. color the module
    - top half = jet black
    - bottom half = ivory white
    '''
    # Switch to Edit Mode
    bpy.context.view_layer.objects.active = module
    bpy.ops.object.mode_set(mode='EDIT')

    # Access the mesh in edit mode
    mesh = bmesh.from_edit_mesh(module.data)

    # Deselect everything first
    for f in mesh.faces:
        f.select = False

    # Select faces where average Z > 0
    for f in mesh.faces:
        avg_z = sum(v.co.z for v in f.verts) / len(f.verts)
        if avg_z > 0:
            f.select = True

    # Update the selection in viewport
    bmesh.update_edit_mesh(module.data, loop_triangles=False, destructive=False)

    # Assign white material (slot 1) to selected faces
    module.active_material_index = 1
    bpy.ops.object.material_slot_assign()

    # Update mesh and return to object mode
    bmesh.update_edit_mesh(module.data, loop_triangles=False, destructive=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    return module


'''
Builds the 1st QR code that is derived from the 1st URL in the user input
'''
def build_initial_qr_code(qr_matrix):
    N = len(qr_matrix)
    n = N - (gv.border * 2)
    gv.qr_matrix_size = n
    gv.qr_matrix_length = N

    gv.qr_matrix_module_names = [
        ['' for _ in range(N)] 
        for _ in range(N)
    ]
    gv.qr_matrix_prev_state = [
        [True for _ in range(N)] 
        for _ in range(N)
    ]

    if gv.will_include_logo:
        m = (n // 3) + (1 if (n // 3) % 2 == 0 else 0)
        i_start = ((N - m) // 2)
        i_end = i_start + m
        
    # iterate through 0 to gv.qr_matrix_size in y direction
    for i in range(0, N):
        
        # iterate through 0 to gv.qr_matrix_size in x direction
        for j in range(0, N):
            
            # duplicate the original module
            module_copy = gv.module.copy()
            module_copy.data = gv.module.data.copy()
            # set the location of the duplicated module
            module_copy.location = (j * 0.1, -i * 0.1, 0)
            # move the module to the "qr-code" collection
            gv.qr_code_coll.objects.link(module_copy)

            # write the module object's name into the global qr_matrix_module_names
            gv.qr_matrix_module_names[i][j] = module_copy.name
            gv.qr_matrix_prev_state[i][j] = qr_matrix[i][j]

            if qr_matrix[i][j] == False: # white
                module_copy.rotation_euler[0] = math.pi

            if gv.will_include_logo:
                if i_start <= i < i_end and i_start <= j < i_end:
                    # hide the current module to create empty center
                    module_copy.hide_set(True)
                    module_copy.hide_render = True


'''
Iterate through the QR code matrix and build the QR code by duplicating the module. 
For each bit, if it's in the center area, skip duplicating the module to create empty center.
Duplicate the module regardless of the bit value, but if the bit is ON, leave it as is, 
so it displays black. Else if the bit is OFF, flip it so it displays white.
'''
def build_qr_code(qr_matrix):
    n = gv.qr_matrix_size
    N = n + (gv.border * 2)
    
    # Deselect all first
    bpy.ops.object.select_all(action='DESELECT')

    # iterate through 0 to gv.qr_matrix_size in y direction
    for i in range(0, N):
        
        # iterate through 0 to gv.qr_matrix_size in x direction
        for j in range(0, N):

            prev_bit = gv.qr_matrix_prev_state[i][j]
            curr_bit = qr_matrix[i][j]
            module_name = gv.qr_matrix_module_names[i][j]
            module_obj = bpy.data.objects.get(module_name)

            if module_obj:
                # Select and make it active
                module_obj.select_set(True)
                bpy.context.view_layer.objects.active = module_obj

                if prev_bit != curr_bit:
                    # Rotate by 180 degrees on X axis (in radians)
                    module_obj.rotation_euler[0] += math.pi
                else:
                    # Rotate by 180 degrees on X axis (in radians)
                    module_obj.rotation_euler[0] += (2 * math.pi)

            else:
                print("Error: module object not found:", module_name)

    gv.qr_matrix_prev_state = qr_matrix
