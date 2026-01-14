import bpy
import qrcode
import math

# Name of the object you want to select
obj_name = "module"

# Deselect everything first
bpy.ops.object.select_all(action='DESELECT')

# Check if object exists
if obj_name in bpy.data.objects:
    module = bpy.data.objects[obj_name]
    module.select_set(True)  # Select it
    bpy.context.view_layer.objects.active = module  # Make it the active object
else:
    print(f"Object '{obj_name}' not found")


data = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Create QR code object
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,
    border=2,  # extra border helps scanners
)
qr.add_data(data)
qr.make(fit=True)

# Get matrix
matrix = qr.get_matrix()

curr_y = 0
curr_x = 0

# Print ASCII QR code
# origin is at top-left corner
for row in matrix:
    # for each row, decrement y by 0.1
    # for each col, increment x by 0.1
    

    # y = row index
    # x = column index

    for col in row:
        # step 1: add icosphere
        module_copy = module.copy()
        module_copy.data = module.data.copy()
        module_copy.location = (curr_x, curr_y, 0)

        if col:
            # black color should face up
            # bpy.ops.object.report(type='INFO', message="black color should face up")
            print("black color should face up")
            
        else:
            # white color should face up
            # bpy.ops.object.report(type='INFO', message="black color should face up")
            print("black color should face up")
            module_copy.rotation_euler[0] = math.pi  # rotate 180 degrees around x-axis

        bpy.context.collection.objects.link(module_copy)

        

            

        # bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.05, location=(curr_x, curr_y, 0)) 
        
        
        # step 2: increment x by 0.1
        curr_x += 0.1

    # at the end of each row, decrement y by 0.1 and reset x to 0
    curr_y -= 0.1
    curr_x = 0

    # line = "".join("██" if col else "  " for col in row)
    # print(line)


# 2. Create a real duplicate with its own mesh data
# module_copy = module.copy()
# module_copy.data = module.data.copy()
# module_copy.name = "module_copy"
# module_copy.location = (0, 0, 0)

# # Link the duplicate to the current collection
# bpy.context.collection.objects.link(module_copy)

'''

import subprocess
import sys
import os
import bpy

# Path to the Blender Python executable
# this is for Windows, will need to adjust for other OS
python_exe = os.path.join(sys.prefix, 'bin', 'python.exe')

# Upgrade pip to the latest version
subprocess.call([python_exe, "-m", "ensurepip"])
subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])

# Install the desired package
subprocess.call([python_exe, "-m", "pip", "install", "qrcode"])

import qrcode

# rickroll ppl data
data = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Create QR code object
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=1,
    border=2,  # extra border helps scanners
)
qr.add_data(data)
qr.make(fit=True)

# Get matrix
matrix = qr.get_matrix()

curr_y = 0
curr_x = 0

# Print ASCII QR code
# origin is at top-left corner
for row in matrix:
    # for each row, decrement y by 0.1
    # for each col, increment x by 0.1
    

    # y = row index
    # x = column index

    for col in row:
        # step 1: add icosphere
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.05, location=(curr_x, curr_y, 0)) 
        
        # step 2: increment x by 0.1
        curr_x += 0.1

    # at the end of each row, decrement y by 0.1 and reset x to 0
    curr_y -= 0.1
    curr_x = 0

    # line = "".join("██" if col else "  " for col in row)
    # print(line)

'''





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
module.active_material_index = 1  # White material slot
bpy.ops.object.material_slot_set(assign=True)

# Switch back to Object Mode
bpy.ops.object.mode_set(mode='OBJECT')


# 2. Create a real duplicate with its own mesh data
module_copy = module.copy()
module_copy.data = module.data.copy()
module_copy.name = "module_copy"
module_copy.location = (3, 0, 0)

# Link the duplicate to the current collection
bpy.context.collection.objects.link(module_copy)
'''