import bpy

# (x,y,z)
verts = [(1,1,-1),(1,-1,-1),(-1,-1,-1),(-1,1,-1),(1,1,1),(1,-1,1),(-1,-1,1),(-1,1,1)]
# Boden, Seiten, Deckel
faces = [(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(4,0,3,7)]

mesh = bpy.data.meshes.new("Cube")
mesh.from_pydata(verts, [], faces)

obj = bpy.data.objects.new("Cube", mesh)
bpy.context.scene.collection.objects.link(obj)

bpy.context.view_layer.objects.active = obj

offset = (0,0,1)

obj.location = [i * -1 for i in offset]

bpy.context.active_object.select_set(state=True)



material_basic = bpy.data.materials.new(name = "Basic")

material_new = bpy.data.materials.get("Basic")

# to get the PBSDF Schader node of the active object:
# bsdf_node =  bpy.context.object.active_material.node_tree.nodes.get("Principled BSDF")

material_basic.use_nodes = True

bpy.context.active_object.active_material = material_basic

bsdf_node = material_basic.node_tree.nodes.get("Principled BSDF")
assert(bsdf_node) # make sure it exists to continue


bsdf_node.inputs[0].default_value = (1.0, 0.0, 0.0, 1.0)
bsdf_node.inputs[7].default_value = 0.69  # Specular
bsdf_node.inputs[9].default_value = 0.26  # Roughnes



# -----------------------------------------------------------------------
#  connect nodes:
# create new Mat
material = bpy.data.materials.new(name = "B")
material.use_nodes = True     #principled bdsf connected to mat-out

# add new Node and set var for bsdf
emission = material.node_tree.nodes.new('ShaderNodeEmission')
bsdf = material.node_tree.nodes.get('Principled BSDF')

# link nodes
material.node_tree.links.new(bsdf.inputs[0], emission.outputs[0])
# -----------------------------------------------------------------------