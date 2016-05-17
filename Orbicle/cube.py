#!/bin/python

# from util import adjacent_pairs
from geometry import *
# Parameters

########################################
# Orbicle
########################################
class Cube(object):
    def __init__(self):
        self.v000 = Point(0,0,0)
        self.v001 = Point(0,0,1)
        self.v010 = Point(0,1,0)
        self.v011 = Point(0,1,1)
        self.v100 = Point(1,0,0)
        self.v101 = Point(1,0,1)
        self.v110 = Point(1,1,0)
        self.v111 = Point(1,1,1)
        self.verts = [ self.v000, self.v001, self.v010, self.v011
                     , self.v100, self.v101, self.v110, self.v111
                     ]

        self.e00x = mk_cyl(self.v000, self.v001)
        self.e01x = mk_cyl(self.v010, self.v011)
        self.e10x = mk_cyl(self.v100, self.v101)
        self.e11x = mk_cyl(self.v110, self.v111)
        self.e0x0 = mk_cyl(self.v000, self.v010)
        self.e0x1 = mk_cyl(self.v001, self.v011)
        self.e1x0 = mk_cyl(self.v100, self.v110)
        self.e1x1 = mk_cyl(self.v101, self.v111)
        self.ex00 = mk_cyl(self.v000, self.v100)
        self.ex01 = mk_cyl(self.v001, self.v101)
        self.ex10 = mk_cyl(self.v010, self.v110)
        self.ex11 = mk_cyl(self.v011, self.v111)
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