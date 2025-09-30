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

# import qrcode

# # rickroll ppl data
# data = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# # Create QR code object
# qr = qrcode.QRCode(
#     version=1,
#     error_correction=qrcode.constants.ERROR_CORRECT_L,
#     box_size=1,
#     border=2,  # extra border helps scanners
# )
# qr.add_data(data)
# qr.make(fit=True)

# # Get matrix
# matrix = qr.get_matrix()

# curr_y = 0
# curr_x = 0

# # Print ASCII QR code
# # origin is at top-left corner
# for row in matrix:
#     # for each row, decrement y by 0.1
#     # for each col, increment x by 0.1
    

#     # y = row index
#     # x = column index

#     for col in row:
#         # step 1: add icosphere
#         bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2, radius=0.05, location=(curr_x, curr_y, 0)) 
        
#         # step 2: increment x by 0.1
#         curr_x += 0.1

#     # at the end of each row, decrement y by 0.1 and reset x to 0
#     curr_y -= 0.1
#     curr_x = 0

#     # line = "".join("██" if col else "  " for col in row)
#     # print(line)