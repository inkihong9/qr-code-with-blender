import bpy

'''
1. create a UV sphere with radius of 5cm at location x = -3m, y = 3m, z = 0m
2. name it stone
'''
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(-3,3,0))
stone = bpy.context.active_object
stone.name = "stone"

'''
# 2. Create a real duplicate with its own mesh data
stone_copy = stone.copy()
stone_copy.data = stone.data.copy()
stone_copy.name = "stone_copy"
stone_copy.location = (3, 0, 0)

# Link the duplicate to the current collection
bpy.context.collection.objects.link(stone_copy)
'''