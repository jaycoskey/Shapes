#!/bin/python
########################################
# Goal: Visualize then 3D-print a particular sphere-like 3D shape.
#       The components are line segments (cylinders) and circles (tori).
########################################
from geometry import *

########################################
# Constants
########################################
phi = (1 + sqrt(5)) / 2  # Golden ratio ~ 1.618034


########################################
# Icosahedron
########################################
class Icosahedron(object):
    def __init__(self):
        self.verts = [ px00, px01, px10, px11
                     , p0y0, p0y1, p1y0, p1y1
                     , p00z, p01z, p10z, p11z
                     ]
        self.faces = [ f1,  f2,  f3,  f4,  f5
                     , f6,  f7,  f8,  f9,  f10
                     , f11, f12, f13, f14, f15
                     , f16, f17, f18, f19, f20
                     ]

########################################
# Define icosahedral vertices
########################################
px00 = Point(0, -1, -phi)
px01 = Point(0, -1,  phi)
px10 = Point(0,  1, -phi)
px11 = Point(0,  1,  phi)

p0y0 = Point(-phi, 0, -1)
p0y1 = Point(-phi, 0,  1)
p1y0 = Point( phi, 0, -1)
p1y1 = Point( phi, 0,  1)

p00z = Point(-1, -phi, 0)
p01z = Point(-1,  phi, 0)
p10z = Point( 1, -phi, 0)
p11z = Point( 1,  phi, 0)

########################################
# Define icosahedral faces
########################################
# TODO: Refactor toward DRY
f1  = Triangle(px00, p10z, p00z)
f2  = Triangle(px00, p00z, p0y0)
f3  = Triangle(px00, p0y0, px10)
f4  = Triangle(px00, px10, p1y0)
f5  = Triangle(px00, p1y0, p10z)

f6  = Triangle(p10z, p1y0, p1y1)
f7  = Triangle(p10z, p1y1, px01)
f8  = Triangle(p10z, px01, p00z)
f9  = Triangle(p00z, px01, p0y1)
f10 = Triangle(p00z, p0y1, p0y0)

f11 = Triangle(p0y0, p0y1, p01z)
f12 = Triangle(p0y0, p01z, px10)
f13 = Triangle(px10, p01z, p11z)
f14 = Triangle(px10, p11z, p1y0)
f15 = Triangle(p1y0, p11z, p1y1)

f16 = Triangle(p1y1, p11z, px11)
f17 = Triangle(p1y1, px11, px01)
f18 = Triangle(px01, px11, p0y1)
f19 = Triangle(p0y1, px11, p01z)
f20 = Triangle(p01z, px11, p11z)


def main():
    print('Hello, world!')

if __name__ == '__main__':
    main()
