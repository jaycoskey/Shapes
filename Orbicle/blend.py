#!/bin/python

import os
import sys

import bpy
# import bpy.ops.mesh
from mathutils import Quaternion

from geometry import *  # Point, Vector
from orbicle import *

sphere_radius = 0.5
test_icosa_edge_radius = 0.1

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
def blender_add_point(point):
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=3
        , size=sphere_radius
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
    loc = average_point([cylinder.center1, cylinder.center2])
    cylinder_dir = 0.5 * (cylinder.center2 - cylinder.center1)
    zunit        = Vector(0,0,1)
    rot_axis     = cylinder_dir.cross(zunit).normalized()
    rot_angle    = angle_between(cylinder_dir, zunit)
    quat_rot     = Quaternion((rot_axis.x, rot_axis.y, rot_axis.z), rot_angle)
    euler_rot    = quat_rot.to_euler()
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=32
        , radius=cylinder.r
        , depth=(cylinder.center2 - cylinder.center1).norm
        # , cap_ends=False
        , view_align=False
        , enter_editmode=False
        , location=(loc.x, loc.y, loc.z)
        , rotation=(euler_rot.x, euler_rot.y, euler_rot.z)  # TODO: Not working yet.
        # layers
        )

# Tori (bpy.ops.mesh.primitive_torus_add):
#     https://www.blender.org/api/blender_python_api_2_57_release/bpy.ops.mesh.html
def blender_add_torus(torus):
    rot = (0.0, 0.0, 0.0)  # TODO
    primitive_torus_add(
        major_radius=torus.major_radius
        , minor_radius=torus.minor_radius
        , major_segments=48
        , minor_segments=12
        , use_abso=False
        , abso_major_rad=1.0  # ???
        , abso_minor_rad=0.5  # ???
        , view_align=False
        , location=torus.center
        , rotation=rot
        )

def blender_write_outfile(filepath):
    bpy.ops.export_mesh.stl(
        filepath=filepath
        , check_existing=True
        , ascii=False
        # , apply_modifiers=True
        )

#    outfile   = open(filepath, 'w')   # file(filepath, 'w')
#    scenes    = bpy.data.scenes  # .active
#    objects   = scenes.objects   # .active
#    mesh_data = objects.getData(mesh=1)
#    for mesh_vert in mesh_data.verts:
#        outfile.write('v %f %f %f\n' % (mesh_vert.co.x, mesh_vert.co.y, mesh_vert.co.z))
#        for mesh_face in mesh_data.faces:
#            outfile.write('f')
#            for mesh_face_vert in mesh_face.v:
#                outfile.write(' %i'.format(mesh_face_vert.index + 1))
#            outfile.write('\n')
#        outfile.close()

def main():
    # print('Hello, world!')
    orb = Orbicle()
    delete_all()
    # TODO: Add tori12
    # TODO: Add tori20
    # TODO: Add hexgrids
    # TODO: Perform unions and adjust thickness as needed
    blender_write_outfile('orbicle.stl')

def delete_all():  #  By Takuro Wada.  See video at https://www.blender.org/conference/2015/presentations/157
    for item in bpy.context.scene.objects:
        bpy.context.scene.objects.unlink(item)
    for item in bpy.data.objects:
        bpy.data.objects.remove(item)
    for item in bpy.data.meshes:
        bpy.data.meshes.remove(item)
    for item in bpy.data.materials:
        bpy.data.materials.remove(item)

def test_cubes():
    delete_all()
    # From cube_example.py, at
    #     http://www.mertl-research.at/ceon/doku.php?id=software:kicad:3d_package_with_blender
    bpy.ops.mesh.primitive_cube_add()                    # Add a cube at the origin.
    bpy.ops.mesh.primitive_cube_add(location=(0, 4, 0))  # Add another cube at a different location.
    blender_write_outfile('test_output.stl')

def test_icosa():
    # print('Hello, world!')
    orb = Orbicle()
    icosa_verts = orb.icosa.verts
    for v in icosa_verts:
        blender_add_point(v)

    r = test_icosa_edge_radius
    face_to_edges = lambda f: [Cylinder(f.a, f.b, r), Cylinder(f.b, f.c, r), Cylinder(f.c, f.a, r)]
    cylinderss = map(face_to_edges, orb.icosa.faces)  # TODO: De-dupe
    icosa_edges = [cyl for cylinders in cylinderss for cyl in cylinders]
    delete_all()
    for cylinder in icosa_edges:
        blender_add_cylinder(cylinder)
    blender_write_outfile('test_icosa_output.stl')

if __name__ == '__main__':
    # test_cubes()
    test_icosa()
    main()
