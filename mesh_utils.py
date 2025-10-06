import bpy


def create_stone():
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(-1,1,0))
    stone = bpy.context.active_object
    stone.name = "stone"
    stone.scale = (1,1,0.3)
