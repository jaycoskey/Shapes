# mat_red     = material_make('Red',     (1,0,0), (1,0,0), 1)
# mat_green   = material_make('Green',   (0,1,0), (0,1,0), 1)
# mat_blue    = material_make('Blue',    (0,0,1), (0,0,1), 1)

# mat_yellow  = material_make('Yellow',  (1,1,0), (1,1,0), 1)
# mat_magenta = material_make('Magenta', (1,0,1), (1,0,1), 1)
# mat_cyan    = material_make('Cyan',    (0,1,1), (0,1,1), 1)

# mat_pink    = material_make('Pink',    (1,     0.7529,0.7961), (1,     0.7529,0.7961), 1)
# mat_purple  = material_make('Purple',  (0.6275,0.1254,0.9412), (0.6275,0.1254,0.9412), 1)
# mat_white   = material_make('White',   (1,1,1), (1,1,1), 1)

# material_set_by_name('tori12',       mat_blue)
# material_set_by_name('tori20',       mat_green)
# material_set_by_name('hexgrid_edge', mat_pink)
# material_set_by_name('hexgrid_vert', mat_red)

# See "makeMaterial" at
#     https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Materials_and_textures
def material_make(name, diffuse, specular, alpha):
    mat                    = bpy.data.materials.new(name)
    mat.diffuse_color      = diffuse
    mat.diffuse_shader     = 'LAMBERT'
    mat.diffuse_intensity  = 1.0
    mat.specular_color     = specular
    mat.specular_shader    = 'COOKTORR'
    mat.specular_intensity = 0.5
    mat.alpha              = alpha
    mat.ambient            = 1
    return mat

def material_set(obj, mat):
    bpy.ops.object.mode_set(mode='OBJECT')
    for mat_slot in obj.material_slots:
        bpy.ops.object.material_slot_remove()
    obj.data.materials.append(mat)

def material_set_by_name(name, mat):
    # bpy.ops.object.editmode_toggle()
    bpy.ops.object.select_all(action='DESELECT')

    # bpy.ops.objects.select_pattern(pattern=name).select_all(action='SELECT')
    # How does the following line treat multiple objects with the same name?
    grp = bpy.data.groups.new(name)
    obj = bpy.data.objects.get(name)
    if (obj):
        print('Found object(s) with name: ' + name)
        obj.select = True
        bpy.context.scene.objects.active = obj
        # TODO: Linking to group should only appear in selected_objects loop.  Duplicating here for testing.
        # grp.objects.link(obj)
        material_set(obj, mat)
    else:
        print('Did not find object with name: ' + name)

    for obj in bpy.context.selected_objects:
        grp.objects.link(obj)
        material_set(obj, mat)
    # bpy.ops.object.editmode_toggle()

def name_material_set(obj, name, mat):
    obj.name = name
    me = obj.data
    me.materials.clear()
    me.materials.append(mat)
