import bpy

# deselect everything first
bpy.ops.object.select_all(action='DESELECT')

'''
iterate through all objects in the scene
if the object is not named "Camera" or "Light", then delete it
'''
for obj in bpy.data.objects:
    if obj.name not in {"Camera", "Light"}:
        bpy.data.objects.remove(obj, do_unlink=True)
