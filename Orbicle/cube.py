#!/usr/local/bin/python3.7
# Note: This file is currently unused.

import os
import sys


sys.path.append(os.path.dirname(__file__))
from geometry import Cylinder, Point3, Vec3
from scene import Scene


class Cube():
    def __init__(self):
        self.v000 = Point3(0,0,0)
        self.v001 = Point3(0,0,1)
        self.v010 = Point3(0,1,0)
        self.v011 = Point3(0,1,1)
        self.v100 = Point3(1,0,0)
        self.v101 = Point3(1,0,1)
        self.v110 = Point3(1,1,0)
        self.v111 = Point3(1,1,1)
        self.verts = [ self.v000, self.v001, self.v010, self.v011
                     , self.v100, self.v101, self.v110, self.v111
                     ]

        self.e00x = Cylinder.make(self.v000, self.v001)
        self.e01x = Cylinder.make(self.v010, self.v011)
        self.e10x = Cylinder.make(self.v100, self.v101)
        self.e11x = Cylinder.make(self.v110, self.v111)
        self.e0x0 = Cylinder.make(self.v000, self.v010)
        self.e0x1 = Cylinder.make(self.v001, self.v011)
        self.e1x0 = Cylinder.make(self.v100, self.v110)
        self.e1x1 = Cylinder.make(self.v101, self.v111)
        self.ex00 = Cylinder.make(self.v000, self.v100)
        self.ex01 = Cylinder.make(self.v001, self.v101)
        self.ex10 = Cylinder.make(self.v010, self.v110)
        self.ex11 = Cylinder.make(self.v011, self.v111)
        self.edges = [ self.e00x, self.e01x, self.e10x, self.e11x
                     , self.e0x0, self.e0x1, self.e1x0, self.e1x1
                     , self.ex00, self.ex01, self.ex10, self.ex11
                     ]

        self.f0xx = [self.v000, self.v001, self.v011, self.v010]
        self.f1xx = [self.v100, self.v110, self.v111, self.v101]
        self.fx0x = [self.v000, self.v100, self.v101, self.v001]
        self.fx1x = [self.v010, self.v011, self.v111, self.v110]
        self.fxx0 = [self.v000, self.v100, self.v110, self.v010]
        self.fxx1 = [self.v001, self.v101, self.v111, self.v011]
        self.faces = [self.f0xx, self.f1xx, self.fx0x, self.fx1x, self.fxx0, self.fxx1]

# ========================================
# Test functions

def test_cube_facetori():
    Scene.clear()
    cube = Cube()
    for v in cube.verts:
        blender_add_point(test_cube_vertex_radius, v)
    for f in cube.faces:
        t = Torus(test_cube_edge_radius, f)
        blender_add_torus(t)
    Scene.write_stl_file('test_cube_facetori.stl')

def test_cube_wireframe():
    Scene.clear()
    cube = Cube()
    for v in cube.verts:
        blender_add_point(test_cube_vertex_radius, v)
    for e in cube.edges:
        blender_add_cylinder(e)
    Scene.write_stl_file('test_cube_wireframe.stl')

# ========================================
if __name__ == '__main__':
    test_cube_facetori()
    test_cube_wireframe()
