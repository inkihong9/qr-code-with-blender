import bpy
from .. import global_vars as gv


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
