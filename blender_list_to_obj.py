import bpy
import os
import colorsys
import dill

def rectToObjk(rect):
    hScale = 1
    r, g, b = rect.avColor
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    gray = 0.299*r + 0.587*g +0.114*b
    gray_2 = 0.2126*r + 0.7152*g + 0.0722*b
    height = gray_2 * hScale
    z_min = -0.2
    z_max = (height/2)
    verts = [(rect.x_min/100, rect.y_min/100, z_min),   # 0
             (rect.x_max/100, rect.y_min/100, z_min),   # 1
             (rect.x_max/100, rect.y_max/100, z_min),   # 2
             (rect.x_min/100, rect.y_max/100, z_min),   # 3
             (rect.x_min/100, rect.y_min/100, z_max),   # 4
             (rect.x_max/100, rect.y_min/100, z_max),   # 5
             (rect.x_max/100, rect.y_max/100, z_max),   # 6
             (rect.x_min/100, rect.y_max/100, z_max)]   # 7
    faces = [(0, 1, 2, 3),
             (4, 7, 6, 5),
             (0, 4, 5, 1),
             (1, 5, 6, 2),
             (2, 6, 7, 3),
             (4, 0, 3, 7)]

    mesh = bpy.data.meshes.new("Cube")
    mesh.from_pydata(verts, [], faces)

    obj = bpy.data.objects.new("Cube", mesh)
    bpy.context.scene.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    bpy.context.active_object.select_set(state=True)

    # get Material
    material_basic = bpy.data.materials.get('Material')
    # assign Material to object
    obj.data.materials.append(material_basic)
    # create vertec_color property
    mesh.vertex_colors.new()
    color_layer = mesh.vertex_colors["Col"]
    # iterate over vertices and set color
    for vert in color_layer.data:
        vert.color = (r,g,b,1)

    bpy.context.active_object.select_set(state=False)
    
dill_file = os.path.join("D:", "blender_test", "Gauguin.dill")
    
with open(dill_file,'rb') as file:
    data = dill.load(file)

data_min = data

i = 0
for rect in data_min:
    print(f"Rectangle #{i}")
    rectToObjk(rect)
    i += 1

for obj in bpy.context.scene.objects:
    if "Cube" in obj.name:
        obj.select_set(True)
bpy.ops.object.join()
bpy.ops.object.modifier_add(type="BEVEL")
bpy.context.object.modifiers['Bevel'].width = 0.01
bpy.ops.object.shade_smooth()
bpy.context.object.data.use_auto_smooth = True