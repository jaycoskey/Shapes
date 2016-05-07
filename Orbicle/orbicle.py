#!/bin/python
########################################
# Goal: Visualize then 3D-print a particular sphere-like 3D shape.
#       The components are line segments (cylinders) and circles (toruses).
########################################

from geometry import *
from icosahedron import *

# Parameters
vertex_radius        = 0.02
vertex_frequency     = 4
edge_radius          = 0.02
torus_minor_radius   = 0.02
torus_major_segments = 90
torus_minor_segments = 18

########################################
# Orbicle
########################################
class Orbicle(object):
    def __init__(self, a, b, r):
        self.icosa = Icosahedron()
        self.hexgrid_verts = []
        self.hexgrid_edges = []
        self.tori12 = []
        self.tori20 = []

    ########################################
    # Add icosahedral-vertex-centered tori
    ########################################
    def setTori12(self):
        self.tori12 = [
            weighted_torus(center=px00, others=(p00z,p10z,p1y0,px10,p0y0))
            , weighted_torus(center=px01, others=(px11,p1y1,p10z,p00z,p0y1))
            , weighted_torus(center=px10, others=(px00,p1y0,p11z,p01z,p0y0))
            , weighted_torus(center=px11, others=(p11z,p1y1,px01,p0y1,p01z))
            , weighted_torus(center=p0y0, others=(p0y1,p00z,px00,px10,p01z))
            , weighted_torus(center=p0y1, others=(px11,px01,p00z,p0y0,p01z))
            , weighted_torus(center=p1y0, others=(p1y1,p11z,px10,px00,p10z))
            , weighted_torus(center=p1y1, others=(px11,p11z,p1y0,p10z,px01))
            , weighted_torus(center=p00z, others=(px01,p10z,px00,p0y0,p0y1))
            , weighted_torus(center=p01z, others=(px11,p0y1,p0y0,px10,p11z))
            , weighted_torus(center=p10z, others=(px01,p1y1,p1y0,px00,p00z))
            , weighted_torus(center=p11z, others=(p01z,px10,p1y0,p1y1,px11))
            ]

    ########################################
    # Add icosahedral-face-centered tori
    ########################################
    @property
    def torus_from_points(self) -> Torus:
        return lambda points: Torus(self.minor_radius, points)

    # TODO: Refactor toward DRY
    def setTori20(self):
        self.tori20 = []

        # Add torus centered around f1  = Face(px00, p10z, p00z)
        self.tori20 += self.torus_from_points(
            weighted_triplet((px00, p10z, p1y0), 6, 1, 2)
            , weighted_triplet((px00, p10z, p1y0), 1, 6, 2)
            , weighted_triplet((px00, p00z, p0y0), 6, 1, 2)
            , weighted_triplet((px00, p00z, p0y0), 1, 6, 2)
            , weighted_triplet((p10z, p00z, px01), 6, 1, 2)
            , weighted_triplet((p10z, p00z, px01), 1, 6, 2)
            )

        # Add torus centered around f2  = Face(px00, p00z, p0y0)
        self.tori20 += self.torus_from_points(
            weighted_triplet((px00, p00z, p10z), 6, 1, 2)
            , weighted_triplet((px00, p00z, p10z), 1, 6, 2)
            , weighted_triplet((px00, p0y0, px10), 6, 1, 2)
            , weighted_triplet((px00, p0y0, px10), 1, 6, 2)
            , weighted_triplet((p00z, p0y0, p0y1), 6, 1, 2)
            , weighted_triplet((p00z, p0y0, p0y1), 1, 6, 2)
            )

        # Add torus centered around f3  = Face(px00, p0y0, px10)
        self.tori20 += self.torus_from_points(
            weighted_triplet((px00, p0y0, p00z), 6, 1, 2)
            , weighted_triplet((px00, p0y0, p00z), 1, 6, 2)
            , weighted_triplet((px00, px10, p1y0), 6, 1, 2)
            , weighted_triplet((px00, px10, p1y0), 1, 6, 2)
            , weighted_triplet((p0y0, px10, p01z), 6, 1, 2)
            , weighted_triplet((p0y0, px10, p01z), 1, 6, 2)
            )

        # Add torus centered around f4  = Face(px00, px10, p1y0)
        self.tori20 += self.torus_from_points(
            weighted_triplet((px00, px10, p0y0), 6, 1, 2)
            , weighted_triplet((px00, px10, p0y0), 1, 6, 2)
            , weighted_triplet((px00, p1y0, p10z), 6, 1, 2)
            , weighted_triplet((px00, p1y0, p10z), 1, 6, 2)
            , weighted_triplet((px10, p1y0, p11z), 6, 1, 2)
            , weighted_triplet((px10, p1y0, p11z), 1, 6, 2)
            )

        # Add torus centered around f5  = Face(px00, p1y0, p10z)
        self.tori20 += self.torus_from_points(
            weighted_triplet((px00, p1y0, px10), 6, 1, 2)
            , weighted_triplet((px00, p1y0, px10), 1, 6, 2)
            , weighted_triplet((px00, p10z, p00z), 6, 1, 2)
            , weighted_triplet((px00, p10z, p00z), 1, 6, 2)
            , weighted_triplet((p1y0, p10z, p1y1), 6, 1, 2)
            , weighted_triplet((p1y0, p10z, p1y1), 1, 6, 2)
            )

        # Add torus centered around f6  = Face(p10z, p1y0, p1y1)
        self.tori20 += self.torus_from_points(
            weighted_triplet((p10z, p1y0, px00), 6, 1, 2)
            , weighted_triplet((p10z, p1y0, px00), 1, 6, 2)
            , weighted_triplet((p10z, p1y1, px01), 6, 1, 2)
            , weighted_triplet((p10z, p1y1, px01), 1, 6, 2)
            , weighted_triplet((p1y0, p1y1, p11z), 6, 1, 2)
            , weighted_triplet((p1y0, p1y1, p11z), 1, 6, 2)
            )

        # Add torus centered around f7  = Face(p10z, p1y1, px01)
        self.tori20 += self.torus_from_points(
            weighted_triplet((p10z, p1y1, p1y0), 6, 1, 2)
            , weighted_triplet((p10z, p1y1, p1y0), 1, 6, 2)
            , weighted_triplet((p10z, px01, p00z), 6, 1, 2)
            , weighted_triplet((p10z, px01, p00z), 1, 6, 2)
            , weighted_triplet((p1y1, px01, px11), 6, 1, 2)
            , weighted_triplet((p1y1, px01, px11), 1, 6, 2)
            )

        # Add torus centered around f8  = Face(p10z, px01, p00z)
        self.tori20 += self.torus_from_points(
            weighted_triplet((p10z, px01, p1y1), 6, 1, 2)
            , weighted_triplet((p10z, px01, p1y1), 1, 6, 2)
            , weighted_triplet((p10z, p00z, px00), 6, 1, 2)
            , weighted_triplet((p10z, p00z, px00), 1, 6, 2)
            , weighted_triplet((px01, p00z, p0y1), 6, 1, 2)
            , weighted_triplet((px01, p00z, p0y1), 1, 6, 2)
            )

        # Add torus centered around f9  = Face(p00z, px01, p0y1)
        self.tori20 += self.torus_from_points(
            weighted_triplet((p00z, px01, p10z), 6, 1, 2)
            , weighted_triplet((p00z, px01, p10z), 1, 6, 2)
            , weighted_triplet((p00z, p0y1, p0y0), 6, 1, 2)
            , weighted_triplet((p00z, p0y1, p0y0), 1, 6, 2)
            , weighted_triplet((px01, p0y1, px11), 6, 1, 2)
            , weighted_triplet((px01, p0y1, px11), 1, 6, 2)
            )

        # Add torus centered around f10 = Face(p00z, p0y1, p0y0)
        self.tori20 += self.torus_from_points(
            weighted_triplet((p00z, p0y1, px01), 6, 1, 2)
            , weighted_triplet((p00z, p0y1, px01), 1, 6, 2)
            , weighted_triplet((p00z, p0y0, px00), 6, 1, 2)
            , weighted_triplet((p00z, p0y0, px00), 1, 6, 2)
            , weighted_triplet((p0y1, p0y0, p01z), 6, 1, 2)
            , weighted_triplet((p0y1, p0y0, p01z), 1, 6, 2)
            )

        # Add torus centered around f11 = Face(p0y0, p0y1, p01z)
        self.tori20 += self.torus_from_points(
            weighted_triplet((p0y0, p0y1, p00z), 6, 1, 2)
            , weighted_triplet((p0y0, p0y1, p00z), 1, 6, 2)
            , weighted_triplet((p0y0, p01z, px10), 6, 1, 2)
            , weighted_triplet((p0y0, p01z, px10), 1, 6, 2)
            , weighted_triplet((p0y1, p01z, px11), 6, 1, 2)
            , weighted_triplet((p0y1, p01z, px11), 1, 6, 2)
            )

        # Add torus centered around f12 = Face(p0y0, p01z, px10)
        self.tori20 += self.torus_from_points(
            weighted_triplet((p0y0, p01z, p0y1), 6, 1, 2)
            , weighted_triplet((p0y0, p01z, p0y1), 1, 6, 2)
            , weighted_triplet((p0y0, px10, px00), 6, 1, 2)
            , weighted_triplet((p0y0, px10, px00), 1, 6, 2)
            , weighted_triplet((p01z, px10, p11z), 6, 1, 2)
            , weighted_triplet((p01z, px10, p11z), 1, 6, 2)
            )

        # Add torus centered around f13 = Face(px10, p01z, p11z)
        self.tori20 += self.torus_from_points(
            weighted_triplet((px10, p01z, p0y0), 6, 1, 2)
            , weighted_triplet((px10, p01z, p0y0), 1, 6, 2)
            , weighted_triplet((px10, p11z, p1y0), 6, 1, 2)
            , weighted_triplet((px10, p11z, p1y0), 1, 6, 2)
            , weighted_triplet((p01z, p11z, px11), 6, 1, 2)
            , weighted_triplet((p01z, p11z, px11), 1, 6, 2)
            )

        # Add torus centered around f14 = Face(px10, p11z, p1y0)
        self.tori20 += self.torus_from_points(
            weighted_triplet((px10, p11z, p01z), 6, 1, 2)
            , weighted_triplet((px10, p11z, p01z), 1, 6, 2)
            , weighted_triplet((px10, p1y0, px00), 6, 1, 2)
            , weighted_triplet((px10, p1y0, px00), 1, 6, 2)
            , weighted_triplet((p11z, p1y0, p1y1), 6, 1, 2)
            , weighted_triplet((p11z, p1y0, p1y1), 1, 6, 2)
            )

        # Add torus centered around f15 = Face(p1y0, p11z, p1y1)
        self.tori20 += self.torus_from_points(
            weighted_triplet((p1y0, p11z, px10), 6, 1, 2)
            , weighted_triplet((p1y0, p11z, px10), 1, 6, 2)
            , weighted_triplet((p1y0, p1y1, p10z), 6, 1, 2)
            , weighted_triplet((p1y0, p1y1, p10z), 1, 6, 2)
            , weighted_triplet((p11z, p1y1, px11), 6, 1, 2)
            , weighted_triplet((p11z, p1y1, px11), 1, 6, 2)
            )

        # Add torus centered around f16 = Face(p1y1, p11z, px11)
        self.tori20 += self.torus_from_points(
            weighted_triplet((p1y1, p11z, p1y0), 6, 1, 2)
            , weighted_triplet((p1y1, p11z, p1y0), 1, 6, 2)
            , weighted_triplet((p1y1, px11, px01), 6, 1, 2)
            , weighted_triplet((p1y1, px11, px01), 1, 6, 2)
            , weighted_triplet((p11z, px11, p01z), 6, 1, 2)
            , weighted_triplet((p11z, px11, p01z), 1, 6, 2)
            )

        # Add torus centered around f17 = Face(p1y1, px11, px01)
        self.tori20 += self.torus_from_points(
            weighted_triplet((p1y1, px11, p11z), 6, 1, 2)
            , weighted_triplet((p1y1, px11, p11z), 1, 6, 2)
            , weighted_triplet((p1y1, px01, p10z), 6, 1, 2)
            , weighted_triplet((p1y1, px01, p10z), 1, 6, 2)
            , weighted_triplet((px11, px01, p0y1), 6, 1, 2)
            , weighted_triplet((px11, px01, p0y1), 1, 6, 2)
            )

        # Add torus centered around f18 = Face(px01, px11, p0y1)
        self.tori20 += self.torus_from_points(
            weighted_triplet((px01, px11, p1y1), 6, 1, 2)
            , weighted_triplet((px01, px11, p1y1), 1, 6, 2)
            , weighted_triplet((px01, p0y1, p00z), 6, 1, 2)
            , weighted_triplet((px01, p0y1, p00z), 1, 6, 2)
            , weighted_triplet((px11, p0y1, p01z), 6, 1, 2)
            , weighted_triplet((px11, p0y1, p01z), 1, 6, 2)
            )

        # Add torus centered around f19 = Face(p0y1, px11, p01z)
        self.tori20 += self.torus_from_points(
            weighted_triplet((p0y1, px11, px01), 6, 1, 2)
            , weighted_triplet((p0y1, px11, px01), 1, 6, 2)
            , weighted_triplet((p0y1, p01z, p0y0), 6, 1, 2)
            , weighted_triplet((p0y1, p01z, p0y0), 1, 6, 2)
            , weighted_triplet((px11, p01z, p11z), 6, 1, 2)
            , weighted_triplet((px11, p01z, p11z), 1, 6, 2)
            )

        # Add torus centered around f20 = Face(p01z, px11, p11z)
        self.tori20 += self.torus_from_points(
            weighted_triplet((p01z, px11, p0y1), 6, 1, 2)
            , weighted_triplet((p01z, px11, p0y1), 1, 6, 2)
            , weighted_triplet((p01z, p11z, px10), 6, 1, 2)
            , weighted_triplet((p01z, p11z, px10), 1, 6, 2)
            , weighted_triplet((px11, p11z, p1y1), 6, 1, 2)
            , weighted_triplet((px11, p11z, p1y1), 1, 6, 2)
            )

#def render_icosa_verts():
#    for v in icosa_verts:
#        mesh.primitive_ico_sphere_add(subdivisions=4, location=v.coordinates(), size= vertex_radius)

########################################
# Add planar hexagons
########################################
def weighted_triplet(ps, w1, w2, w3):
    (p1, p2, p3) = ps
    sumOfWeights = w1 + w2 + w3
    weights = (w1, w2, w3) / sum
    coords_x = (p1.x, p2.x, p3.x)
    coords_y = (p1.y, p2.y, p3.y)
    coords_z = (p1.z, p2.z, p3.z)
    return (coords_x.dot(weights), coords_y.dot(weights), coords_z.dot(weights))


# def hexagon_add(hv1, hv2, hv3, hv4, hv5, hv6):
#     pipe_add(hv1, hv2)
#     pipe_add(hv2, hv3)
#     pipe_add(hv3, hv4)
#     pipe_add(hv4, hv5)
#     pipe_add(hv5, hv6)
#     pipe_add(hv6, hv1)
#
# # TODO: Refactor toward DRY
# for face in icosa_faces:
#     a = face.p1
#     b = face.p2
#     c = face.p3
#     triplet = (a, b, c)
#     add_poly_cylinder(hexgrid_edges,	# Centered around 5, 2, 2
#    	    weighted_triplet(triplet, 6, 2, 1),
#    	    weighted_triplet(triplet, 6, 1, 2),
#    	    weighted_triplet(triplet, 5, 1, 3),
#    	    weighted_triplet(triplet, 4, 2, 3),
#    	    weighted_triplet(triplet, 4, 3, 2),
#    	    weighted_triplet(triplet, 5, 3, 1))
#     add_poly_cylinder(hexgrid_edges,	# Centered around 4, 1, 4
#    	    weighted_triplet(triplet, 5, 1, 3),
#    	    weighted_triplet(triplet, 5, 0, 4),
#    	    weighted_triplet(triplet, 4, 0, 5),
#    	    weighted_triplet(triplet, 3, 1, 5),
#    	    weighted_triplet(triplet, 3, 2, 4),
#    	    weighted_triplet(triplet, 4, 2, 3))
#     add_poly_cylinder(hexgrid_edges,	# Centered around 2, 2, 5
#    	    weighted_triplet(triplet, 3, 2, 4),
#    	    weighted_triplet(triplet, 3, 1, 5),
#    	    weighted_triplet(triplet, 2, 1, 6),
#    	    weighted_triplet(triplet, 1, 2, 6),
#    	    weighted_triplet(triplet, 1, 3, 5),
#    	    weighted_triplet(triplet, 2, 3, 4))
#     add_poly_cylinder(hexgrid_edges,	# Centered around 1, 4, 4
#    	    weighted_triplet(triplet, 2, 4, 3),
#    	    weighted_triplet(triplet, 2, 3, 4),
#    	    weighted_triplet(triplet, 1, 3, 5),
#    	    weighted_triplet(triplet, 0, 4, 5),
#    	    weighted_triplet(triplet, 0, 5, 4),
#    	    weighted_triplet(triplet, 1, 5, 3))
#     add_poly_cylinder(hexgrid_edges,	# Centered around 2, 5, 2
#    	    weighted_triplet(triplet, 3, 5, 1),
#    	    weighted_triplet(triplet, 3, 4, 2),
#    	    weighted_triplet(triplet, 2, 4, 3),
#    	    weighted_triplet(triplet, 1, 5, 3),
#    	    weighted_triplet(triplet, 1, 6, 2),
#    	    weighted_triplet(triplet, 2, 6, 1))
#     add_poly_cylinder(hexgrid_edges,	# Centered around 4, 4, 1
#    	    weighted_triplet(triplet, 5, 4, 0),
#    	    weighted_triplet(triplet, 5, 3, 1),
#    	    weighted_triplet(triplet, 4, 3, 2),
#    	    weighted_triplet(triplet, 3, 4, 2),
#    	    weighted_triplet(triplet, 3, 5, 1),
#    	    weighted_triplet(triplet, 4, 5, 0))

def weight_4_5(center):
    return lambda other: (4/9) * center + (5/9) * other

def weighted_torus(center, others):
    return Torus(map(weight_4_5(center), others))

def main():
    print('Hello, world!')

if __name__ == '__main__':
    main()
