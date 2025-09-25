import bpy

# adds an icosphere with subdivision = 3, radius of 1 meter at the origin (x=0, y=0, z=0), units are in meters by default
bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=3, radius=1.0, location=(0, 0, 0)) 