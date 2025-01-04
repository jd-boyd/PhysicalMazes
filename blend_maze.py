import bpy
import math
import json


def create_cylinder(location, rotation, radius=0.1, depth=2.0):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=radius, depth=depth, location=location, rotation=rotation)
    return bpy.context.object

def create_sphere(location, radius=0.2):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    return bpy.context.object

# Define a function to apply a Boolean Union
def boolean_union(target, to_union):
    bpy.context.view_layer.objects.active = target
    boolean_modifier = target.modifiers.new(name="Union", type='BOOLEAN')
    boolean_modifier.operation = 'UNION'
    boolean_modifier.object = to_union
    bpy.ops.object.modifier_apply(modifier=boolean_modifier.name)
    bpy.data.objects.remove(to_union, do_unlink=True)


#collection_name = "MyMaze"
#new_collection = bpy.data.collections.new(collection_name)
#bpy.context.scene.collection.children.link(new_collection)


bpy.ops.mesh.primitive_cube_add(scale=(5, 5, 0.2), location=(4.5, 4.5, 0.75))
cube = bpy.context.object
#new_collection.objects.link(cube)
#bpy.context.scene.collection.objects.unlink(cube)


with open("c:/users/jdboyd/Downloads/maze (1).json") as fh:
    raw_data = fh.read()

json_data = json.loads(raw_data)

balls = []
cyls = []

def make_cell(cell):
    ball = create_sphere((cell['i'], cell['j'], 0.5), 0.25)
    balls.append(ball)
    #top
#    if not cell['walls'][0]:
#        print("Connect top")
#        c = create_cylinder((cell['i'], cell['j']-0.25, 0.5),
#                 (math.radians(90), 0, 0), radius=0.25, depth=0.5)
#        c["side"]="Top"
#        c["pos"]=(cell['i'], cell['j'])
#        cyls.append(c)
    #right
    if not cell['walls'][1]:
        print("Connect right")
        c = create_cylinder((cell['i']+0.5, cell['j'], 0.5),
                 (0, math.radians(90), 0), radius=0.25, depth=1.0)
        c["side"]="Right"
        c["pos"]=(cell['i'], cell['j'])
        cyls.append(c)
    #bottom
    if not cell['walls'][2]:
        print("Connect bottom")
        c = create_cylinder((cell['i'], cell['j']+0.5, 0.5),
                 (-math.radians(90), 0, 0), radius=0.25, depth=1.0)
        c["side"]="Bottom"
        c["pos"]=(cell['i'], cell['j'])
        cyls.append(c)
    #left
#    if not cell['walls'][3]:
#        print("Connect left")
#        c = create_cylinder((cell['i']-0.25, cell['j'], 0.5),
#                 (0, math.radians(90), 0), radius=0.25, depth=0.5)
#        c["side"]="Left"
#        c["pos"]=(cell['i'], cell['j'])
#        cyls.append(c)

for cell in json_data:
    make_cell(cell)

new_collection = bpy.data.collections.new("TrackCollection")
bpy.context.scene.collection.children.link(new_collection)
#new_collection.hide_viewport = True

for b in balls[0:]:
    bpy.context.scene.collection.objects.unlink(b)
    bpy.context.scene.collection.children["TrackCollection"].objects.link(b)
    b.select_set(True)

for c in cyls:
    bpy.context.scene.collection.objects.unlink(c)
    bpy.context.scene.collection.children["TrackCollection"].objects.link(c)
    c.select_set(True)


cube.modifiers.new(name="TrackCut", type='BOOLEAN')
cube.modifiers["TrackCut"].operation = 'DIFFERENCE'
cube.modifiers["TrackCut"].operand_type = 'COLLECTION'
cube.modifiers["TrackCut"].collection = new_collection


bpy.context.view_layer.objects.active = cube
bpy.ops.object.modifier_apply(modifier="TrackCut")

for b in balls:
    bpy.data.objects.remove(b, do_unlink=True)

for c in cyls:
    bpy.data.objects.remove(c, do_unlink=True)

#cube.modifiers["TrackCut"].solver = "FAST"
#cube.modifiers["TrackCut"].use_self = True


#bpy.ops.outliner.item_activate(deselect_all=True)
#bpy.ops.outliner.delete(hierarchy=True)
