import bpy


'''
create a single stone and return the object
location param is a tuple of (x, y, z) coordinates
'''
def create_stone(name:str, scale:tuple, location:tuple):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=location)
    stone = bpy.context.active_object
    stone.name = name
    stone.scale = scale
    return stone
