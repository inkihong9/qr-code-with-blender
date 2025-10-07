import bpy


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
    qr_code_coll = bpy.data.collections['qr-code']
    qr_code_coll.objects.link(stone)
 
    return stone


'''
iterate through the QR code matrix and build the QR code by duplicating the correct stone (black or white) at the correct location
qr_matrix param is a 2D list of booleans representing the QR code
white_stone param is the white stone object to duplicate
black_stone param is the black stone object to duplicate
'''
def build_qr_code(qr_matrix, white_stone, black_stone):
    curr_y = 0
    curr_x = 0

    for row in qr_matrix:
        stone_copy = None
        for col in row:
            if col:
                # duplicate black stone
                stone_copy = black_stone.copy()
                stone_copy.data = black_stone.data.copy()
            else:
                # duplicate white stone
                stone_copy = white_stone.copy()
                stone_copy.data = white_stone.data.copy()

            stone_copy.location = (curr_x, curr_y, 0)

            # move the stone to the "qr-code" collection
            qr_code_coll = bpy.data.collections['qr-code']
            qr_code_coll.objects.link(stone_copy)

            
            bpy.context.collection.objects.unlink(stone_copy)
            curr_x += 0.1

        # at the end of each row, decrement y by 0.1 and reset x to 0
        curr_y -= 0.1
        curr_x = 0
