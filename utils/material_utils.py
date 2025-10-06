import bpy


'''
create a material with given name and color
name param is the material name
color param is a tuple of (R, G, B, A) values ranging from 0 to 1
'''
def create_material(name:str, color:tuple):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = color
    return mat
