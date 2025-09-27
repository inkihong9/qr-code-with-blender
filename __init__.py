bl_info = {
    "name": "hey whats up",
    "author": "Your Name",
    "version": (1, 0),
    "blender": (4, 5, 0),
    "location": "View3D > Sidebar",
    "description": "A very simple example addon",
    "category": "Object",
}

import bpy

class SimpleOperator(bpy.types.Operator):
    bl_idname = "object.simple_operator"
    bl_label = "Simple Operator"

    def execute(self, context):
        self.report({'INFO'}, "Hello Blender!")
        print("Hello Blender!")
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(SimpleOperator.bl_idname)

def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
