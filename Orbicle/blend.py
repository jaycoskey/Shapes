#!/bin/python

import sys
from itertools import chain

# Blender Python
import bpy
# import bpy.ops.mesh
from mathutils import Quaternion

# Orbicle
from cube import *
from orbicle import *

# Three ways to create objects:
#     https://wiki.blender.org/index.php/Dev:Py/Scripts/Cookbook/Code_snippets/Three_ways_to_create_objects
# Creating a 3D model using Python:
#     http://www.mertl-research.at/ceon/doku.php?id=software:kicad:3d_package_with_blender
#
# Preparing Blender files for 3D Printing:
#     http://www.shapeways.com/tutorials/prepping_blender_files_for_3d_printing
# Reduction/Decimation:
#     https://wiki.blender.org/index.php/Extensions:2.4/Py/Scripts/Mesh/Mesh_poly_reduce

# Spheres (bpy.ops.mesh.primitive_ico_sphere_add):
#     https://www.blender.org/api/blender_python_api_2_57_release/bpy.ops.mesh.html
def blender_add_point(r, point):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=3
        , size=r
        , view_align=False
        , enter_editmode=False
        , location=(point.x, point.y, point.z)
        # rotation=(0.0, 0.0, 0.0)  # Not needed
        # layers
        )

# Cylinders (bpy.ops.mesh.primitive_cylinder_add):
#     https://www.blender.org/api/blender_python_api_2_57_release/bpy.ops.mesh.html
# or use a beveled pair of circles, as explained at
#     http://blender.stackexchange.com/questions/5898/how-can-i-create-a-cylinder-linking-two-points-with-python
#         bpy.ops.curve.primitive_bezier_circle_add()    #for blending
#         obj = bpy.context.object
#         bpy.ops.curve.primitive_bezier_curve_add()     # a curve, your endpoints for example
#         bpy.context.object.data.bevel_object = bpy.data.objects[obj.name] #a cylinder
#     Documentation on primitive_bezier_circle_add can be found at:
#         https://www.blender.org/api/blender_python_api_2_59_2/bpy.ops.curve.html
def blender_add_cylinder(cylinder):
    loc          = average_point([cylinder.center1, cylinder.center2])
    zunit        = Vector(0, 0, 1)
    cylinder_dir = 0.5 * (cylinder.center2 - cylinder.center1)
    euler_rot    = vectors2euler(zunit, cylinder_dir)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices         = 32
        , radius         = cylinder.r
        , depth          = (cylinder.center2 - cylinder.center1).norm
        # , cap_ends=False
        , view_align     = False
        , enter_editmode = False
        , location       = (loc.x, loc.y, loc.z)
        , rotation       = (euler_rot.x, euler_rot.y, euler_rot.z)
        # layers
        )

# Tori (bpy.ops.mesh.primitive_torus_add):
#     https://www.blender.org/api/blender_python_api_2_57_release/bpy.ops.mesh.html
def blender_add_torus(torus):
    zunit   = Vector(0, 0, 1)
    euler_rot = vectors2euler(zunit, torus.normal)
    bpy.ops.mesh.primitive_torus_add(
        major_radius=torus.major_radius
        , minor_radius=torus.minor_radius
        , major_segments=48
        , minor_segments=12
        # , use_abso=False
        , abso_major_rad=1.0  # TODO: ???
        , abso_minor_rad=0.5  # TODO: ???
        , view_align=False
        , location=(torus.center.x, torus.center.y, torus.center.z)
        , rotation=(euler_rot.x, euler_rot.y, euler_rot.z)
        )

def blender_write_outfile(filepath):
    bpy.ops.export_mesh.stl(
        filepath=filepath
        , check_existing=True
        , ascii=False
        # , apply_modifiers=True
        )

def delete_all():  #  By Takuro Wada.  See video at https://www.blender.org/conference/2015/presentations/157
    for item in bpy.context.scene.objects:
        bpy.context.scene.objects.unlink(item)
    for item in bpy.data.objects:
        bpy.data.objects.remove(item)
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)

def progress(done=False):
    if done:
        print('')
    else:
        print('.', end='')

def vectors2euler(vec_ref, vec_actual):
    rot_axis  = vec_ref.cross(vec_actual).normalized()
    rot_angle = angle_between(vec_actual, vec_ref)
    quat_rot  = Quaternion((rot_axis.x, rot_axis.y, rot_axis.z), rot_angle)
    euler_rot = quat_rot.to_euler()
    return euler_rot

# Note: Duplicate verts/edges/faces can be deduped more easily in Blender than in Python.
def main():
    sys.stdout.flush()
    # Inefficient means of putting seperate parts of the orbicle into separate STL files.
    orb = Orbicle()

    delete_all()
    for t in orb.tori12:
       blender_add_torus(t);     progress()
    progress(done=True)
    blender_write_outfile('orbicle_tori12.stl')

    delete_all()
    for t in orb.tori20:
        blender_add_torus(t);    progress()
    progress(done=True)
    blender_write_outfile('orbicle_tori20.stl')

    delete_all()
    for hv in orb.hexgrid_verts:
       r = hexgrid_vertex_radius
       blender_add_point(r, hv);  progress()
    progress(done=True)
    blender_write_outfile('orbicle_hexgrid_verts.stl')

    delete_all()
    for he in orb.hexgrid_edges:
        blender_add_cylinder(he);    progress()
    progress(done=True)
    blender_write_outfile('orbicle_hexgrid_edges.stl')

    # blender_write_outfile('orbicle.stl')

########################################
# TEST CODE
########################################
def test_cube_facetori():
    delete_all()
    cube = Cube()
    for v in cube.verts:
        blender_add_point(test_cube_vertex_radius, v)
    for f in cube.faces:
        t = Torus(test_cube_edge_radius, f)
        blender_add_torus(t)
    blender_write_outfile('test_cube_facetori.stl')

def test_cube_wireframe():
    delete_all()
    cube = Cube()
    for v in cube.verts:
        blender_add_point(test_cube_vertex_radius, v)
    for e in cube.edges:
        blender_add_cylinder(e)
    blender_write_outfile('test_cube_wireframe.stl')

def test_icosa_wireframe():
    delete_all()
    orb = Orbicle()
    icosa_verts = orb.icosa.verts
    for v in icosa_verts:
        blender_add_point(test_icosa_vertex_radius, v)

    r = test_icosa_edge_radius
    f2e = lambda f: [ Cylinder(f.a, f.b, r)
                    , Cylinder(f.b, f.c, r)
                    , Cylinder(f.c, f.a, r)
                    ]
    # Note: This duplicates edges.  OK, because it's only a test.
    icosa_edgess = map(f2e, orb.icosa.faces)
    icosa_edges  = list(chain.from_iterable(icosa_edgess))
    for e in icosa_edges:
        blender_add_cylinder(e)
    blender_write_outfile('test_icosa_wireframe.stl')


########################################
# MAIN
########################################
if __name__ == '__main__':
    main()
    test_cube_facetori()
    test_cube_wireframe()
    test_icosa_wireframe()
