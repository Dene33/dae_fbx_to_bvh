import bpy
import os


def export_bvh(file):
    bpy.ops.object.select_all(action='TOGGLE')

    obj = scene.objects.get(bpy.data.armatures[0].name)
    if obj != None:
        obj.select = True
        scene.objects.active = obj

    #cont = bpy.context.area.type
    #print(str(cont))

    frame_start = 1
    frame_end = 100

    if bpy.data.actions:
        # get all actions
        action_list = [action.frame_range for action in bpy.data.actions]
        frame_end = action_list[-1][-1]

    bpy.ops.export_anim.bvh(filepath=directory + '\\' +
                            file[:-4] + '.bvh', frame_start=frame_start, frame_end=frame_end)

    bpy.ops.object.select_all(action='TOGGLE')
    bpy.ops.object.select_all(action='TOGGLE')

    bpy.ops.object.delete(use_global=False)
    print('Exported:'+file)


scene = bpy.context.scene

filepath = bpy.data.filepath
directory = os.path.dirname(filepath)

for obj in bpy.context.scene.objects:
    if obj.type == 'ARMATURE':
        obj.select = True
    else:
        obj.select = False
bpy.ops.object.delete()

for block in bpy.data.armatures:
    if block.users == 0:
        bpy.data.armatures.remove(block)

for block in bpy.data.actions:
    if block.users == 0:
        bpy.data.actions.remove(block)

for file in os.listdir(directory):
    if file.endswith('.dae'):
        bpy.ops.wm.collada_import(filepath=directory+'\\' + file,
                                  fix_orientation=True,
                                  find_chains=True)
        export_bvh(file)

    elif file.endswith('.fbx'):
        bpy.ops.import_scene.fbx(filepath=directory+'\\' + file,
                                 automatic_bone_orientation=True,
                                 ignore_leaf_bones=True)
        export_bvh(file)
