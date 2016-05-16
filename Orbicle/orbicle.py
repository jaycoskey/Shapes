#!/bin/python
########################################
# Goal: Visualize then 3D-print a particular sphere-like 3D shape.
#       The components are line segments (cylinders) and circles (toruses).
########################################

from util import adjacent_pairs
# from geometry import *
from icosahedron import *

########################################
# Orbicle
########################################
class Orbicle(object):
    def __init__(self):
        self.icosa = Icosahedron()
        self.tori12 = []
        self.tori20 = []
        self.hexgrid_verts = []
        self.hexgrid_edges = []
        self.set_tori12()
        self.set_tori20()
        self.set_hexgrid()

    ########################################
    # Add hexgrids
    ########################################
    def print(self):
        print('12 (smaller) vertex-centered tori')
        for t12 in self.tori12:
            print(t12)
        print()
        print('20 (larger) face-centered tori')
        for t20 in self.tori20:
            print(t20)
        #for hv in self.hexgrid_verts:
        #    print(hv)
        #for he in self.hexgrid_edges:
        #    print(he)

    def set_hexgrid(self):
        self.hexgrid_verts = []
        self.hexgrid_edges = []
        # TODO: Refactor toward DRY
        for face in self.icosa.faces:
            a = face.a
            b = face.b
            c = face.c
            triplet = (a, b, c)
            # For each icosahedron fact, add 6 hexagons explicitly.
            # The one hexagon in the center is added implicitly,
            #     since it shares its edges with the surrounding hexagons.
            # Identify the hexagons by the hexgrid coords of the vertex they surround.
            #
            # Centered around 5, 2, 2
            wts_522 = [ weighted_point(triplet, (6, 2, 1))
                      , weighted_point(triplet, (6, 1, 2))
                      , weighted_point(triplet, (5, 1, 3))
                      , weighted_point(triplet, (4, 2, 3))
                      , weighted_point(triplet, (4, 3, 2))
                      , weighted_point(triplet, (5, 3, 1))
                      ]

            # Centered around 4, 1, 4
            wts_414 = [ weighted_point(triplet, (5, 1, 3))
                      , weighted_point(triplet, (5, 0, 4))
                      , weighted_point(triplet, (4, 0, 5))
                      , weighted_point(triplet, (3, 1, 5))
                      , weighted_point(triplet, (3, 2, 4))
                      , weighted_point(triplet, (4, 2, 3))
                      ]

            # Centered around 2, 2, 5
            wts_225 = [ weighted_point(triplet, (3, 2, 4))
                      , weighted_point(triplet, (3, 1, 5))
                      , weighted_point(triplet, (2, 1, 6))
                      , weighted_point(triplet, (1, 2, 6))
                      , weighted_point(triplet, (1, 3, 5))
                      , weighted_point(triplet, (2, 3, 4))
                      ]

            # Centered around 1, 4, 4
            wts_144 = [ weighted_point(triplet, (2, 4, 3))
                      , weighted_point(triplet, (2, 3, 4))
                      , weighted_point(triplet, (1, 3, 5))
                      , weighted_point(triplet, (0, 4, 5))
                      , weighted_point(triplet, (0, 5, 4))
                      , weighted_point(triplet, (1, 5, 3))
                      ]

            # Centered around 2, 5, 2
            wts_252 = [ weighted_point(triplet, (3, 5, 1))
                      , weighted_point(triplet, (3, 4, 2))
                      , weighted_point(triplet, (2, 4, 3))
                      , weighted_point(triplet, (1, 5, 3))
                      , weighted_point(triplet, (1, 6, 2))
                      , weighted_point(triplet, (2, 6, 1))
                      ]

            # Centered around 4, 4, 1
            wts_441 = [ weighted_point(triplet, (5, 4, 0))
                      , weighted_point(triplet, (5, 3, 1))
                      , weighted_point(triplet, (4, 3, 2))
                      , weighted_point(triplet, (3, 4, 2))
                      , weighted_point(triplet, (3, 5, 1))
                      , weighted_point(triplet, (4, 5, 0))
                      ]

            hexagons = [wts_522, wts_414, wts_225, wts_144, wts_252, wts_441]
            for hexagon in hexagons:
                for v in hexagon:
                    self.hexgrid_verts.append(v)
                for (v1, v2) in adjacent_pairs(hexagon):
                    self.hexgrid_edges.append(Cylinder(v1, v2, hexgrid_edge_radius))

            # De-dupe vertices.
            # TODO: Add vertices in the weighted triplets
            # TODO: Add edges connecting the weighted triplets

    ########################################
    # Add icosahedral-vertex-centered tori
    ########################################
    def set_tori12(self):
        self.tori12 = [
            weighted_torus12(center=px00, others=[p00z, p10z, p1y0, px10, p0y0])
            , weighted_torus12(center=px01, others=[px11, p1y1, p10z, p00z, p0y1])
            , weighted_torus12(center=px10, others=[px00, p1y0, p11z, p01z, p0y0])
            , weighted_torus12(center=px11, others=[p11z, p1y1, px01, p0y1, p01z])
            , weighted_torus12(center=p0y0, others=[p0y1, p00z, px00, px10, p01z])
            , weighted_torus12(center=p0y1, others=[px11, px01, p00z, p0y0, p01z])
            , weighted_torus12(center=p1y0, others=[p1y1, p11z, px10, px00, p10z])
            , weighted_torus12(center=p1y1, others=[px11, p11z, p1y0, p10z, px01])
            , weighted_torus12(center=p00z, others=[px01, p10z, px00, p0y0, p0y1])
            , weighted_torus12(center=p01z, others=[px11, p0y1, p0y0, px10, p11z])
            , weighted_torus12(center=p10z, others=[px01, p1y1, p1y0, px00, p00z])
            , weighted_torus12(center=p11z, others=[p01z, px10, p1y0, p1y1, px11])
        ]

    ########################################
    # Add icosahedral-face-centered tori
    ########################################
    # TODO: Refactor toward DRY
    def set_tori20(self):
        # Add torus centered around f1  = Face(px00, p10z, p00z)
        wpoints1 = [ weighted_point((px00, p10z, p1y0), (6, 1, 2))
                   , weighted_point((px00, p10z, p1y0), (1, 6, 2))
                   , weighted_point((px00, p00z, p0y0), (6, 1, 2))
                   , weighted_point((px00, p00z, p0y0), (1, 6, 2))
                   , weighted_point((p10z, p00z, px01), (6, 1, 2))
                   , weighted_point((p10z, p00z, px01), (1, 6, 2))
                   ]
        t1 = torus20_from_points(wpoints1)

        # Add torus centered around f2  = Face(px00, p00z, p0y0)
        wpoints2 = [ weighted_point((px00, p00z, p10z), (6, 1, 2))
                   , weighted_point((px00, p00z, p10z), (1, 6, 2))
                   , weighted_point((px00, p0y0, px10), (6, 1, 2))
                   , weighted_point((px00, p0y0, px10), (1, 6, 2))
                   , weighted_point((p00z, p0y0, p0y1), (6, 1, 2))
                   , weighted_point((p00z, p0y0, p0y1), (1, 6, 2))
                   ]
        t2 = torus20_from_points(wpoints2)

        # Add torus centered around f3  = Face(px00, p0y0, px10)
        wpoints3 = [ weighted_point((px00, p0y0, p00z), (6, 1, 2))
                   , weighted_point((px00, p0y0, p00z), (1, 6, 2))
                   , weighted_point((px00, px10, p1y0), (6, 1, 2))
                   , weighted_point((px00, px10, p1y0), (1, 6, 2))
                   , weighted_point((p0y0, px10, p01z), (6, 1, 2))
                   , weighted_point((p0y0, px10, p01z), (1, 6, 2))
                   ]
        t3 = torus20_from_points(wpoints3)

        # Add torus centered around f4  = Face(px00, px10, p1y0)
        wpoints4 = [ weighted_point((px00, px10, p0y0), (6, 1, 2))
                   , weighted_point((px00, px10, p0y0), (1, 6, 2))
                   , weighted_point((px00, p1y0, p10z), (6, 1, 2))
                   , weighted_point((px00, p1y0, p10z), (1, 6, 2))
                   , weighted_point((px10, p1y0, p11z), (6, 1, 2))
                   , weighted_point((px10, p1y0, p11z), (1, 6, 2))
                   ]
        t4 = torus20_from_points(wpoints4)

        # Add torus centered around f5  = Face(px00, p1y0, p10z)
        wpoints5 = [ weighted_point((px00, p1y0, px10), (6, 1, 2))
                   , weighted_point((px00, p1y0, px10), (1, 6, 2))
                   , weighted_point((px00, p10z, p00z), (6, 1, 2))
                   , weighted_point((px00, p10z, p00z), (1, 6, 2))
                   , weighted_point((p1y0, p10z, p1y1), (6, 1, 2))
                   , weighted_point((p1y0, p10z, p1y1), (1, 6, 2))
                   ]
        t5 = torus20_from_points(wpoints5)

        # Add torus centered around f6  = Face(p10z, p1y0, p1y1)
        wpoints6 = [ weighted_point((p10z, p1y0, px00), (6, 1, 2))
                   , weighted_point((p10z, p1y0, px00), (1, 6, 2))
                   , weighted_point((p10z, p1y1, px01), (6, 1, 2))
                   , weighted_point((p10z, p1y1, px01), (1, 6, 2))
                   , weighted_point((p1y0, p1y1, p11z), (6, 1, 2))
                   , weighted_point((p1y0, p1y1, p11z), (1, 6, 2))
                   ]
        t6 = torus20_from_points(wpoints6)

        # Add torus centered around f7  = Face(p10z, p1y1, px01)
        wpoints7 = [ weighted_point((p10z, p1y1, p1y0), (6, 1, 2))
                   , weighted_point((p10z, p1y1, p1y0), (1, 6, 2))
                   , weighted_point((p10z, px01, p00z), (6, 1, 2))
                   , weighted_point((p10z, px01, p00z), (1, 6, 2))
                   , weighted_point((p1y1, px01, px11), (6, 1, 2))
                   , weighted_point((p1y1, px01, px11), (1, 6, 2))
                   ]
        t7 = torus20_from_points(wpoints7)

        # Add torus centered around f8  = Face(p10z, px01, p00z)
        wpoints8 = [ weighted_point((p10z, px01, p1y1), (6, 1, 2))
                   , weighted_point((p10z, px01, p1y1), (1, 6, 2))
                   , weighted_point((p10z, p00z, px00), (6, 1, 2))
                   , weighted_point((p10z, p00z, px00), (1, 6, 2))
                   , weighted_point((px01, p00z, p0y1), (6, 1, 2))
                   , weighted_point((px01, p00z, p0y1), (1, 6, 2))
                   ]
        t8 = torus20_from_points(wpoints8)

        # Add torus centered around f9  = Face(p00z, px01, p0y1)
        wpoints9 = [ weighted_point((p00z, px01, p10z), (6, 1, 2))
                   , weighted_point((p00z, px01, p10z), (1, 6, 2))
                   , weighted_point((p00z, p0y1, p0y0), (6, 1, 2))
                   , weighted_point((p00z, p0y1, p0y0), (1, 6, 2))
                   , weighted_point((px01, p0y1, px11), (6, 1, 2))
                   , weighted_point((px01, p0y1, px11), (1, 6, 2))
                   ]
        t9 = torus20_from_points(wpoints9)

        # Add torus centered around f10 = Face(p00z, p0y1, p0y0)
        wpoints10 = [ weighted_point((p00z, p0y1, px01), (6, 1, 2))
                    , weighted_point((p00z, p0y1, px01), (1, 6, 2))
                    , weighted_point((p00z, p0y0, px00), (6, 1, 2))
                    , weighted_point((p00z, p0y0, px00), (1, 6, 2))
                    , weighted_point((p0y1, p0y0, p01z), (6, 1, 2))
                    , weighted_point((p0y1, p0y0, p01z), (1, 6, 2))
                    ]
        t10 = torus20_from_points(wpoints10)

        # Add torus centered around f11 = Face(p0y0, p0y1, p01z)
        wpoints11 = [ weighted_point((p0y0, p0y1, p00z), (6, 1, 2))
                    , weighted_point((p0y0, p0y1, p00z), (1, 6, 2))
                    , weighted_point((p0y0, p01z, px10), (6, 1, 2))
                    , weighted_point((p0y0, p01z, px10), (1, 6, 2))
                    , weighted_point((p0y1, p01z, px11), (6, 1, 2))
                    , weighted_point((p0y1, p01z, px11), (1, 6, 2))
                    ]
        t11 = torus20_from_points(wpoints11)

        # Add torus centered around f12 = Face(p0y0, p01z, px10)
        wpoints12 = [ weighted_point((p0y0, p01z, p0y1), (6, 1, 2))
                    , weighted_point((p0y0, p01z, p0y1), (1, 6, 2))
                    , weighted_point((p0y0, px10, px00), (6, 1, 2))
                    , weighted_point((p0y0, px10, px00), (1, 6, 2))
                    , weighted_point((p01z, px10, p11z), (6, 1, 2))
                    , weighted_point((p01z, px10, p11z), (1, 6, 2))
                    ]
        t12 = torus20_from_points(wpoints12)

        # Add torus centered around f13 = Face(px10, p01z, p11z)
        wpoints13 = [ weighted_point((px10, p01z, p0y0), (6, 1, 2))
                    , weighted_point((px10, p01z, p0y0), (1, 6, 2))
                    , weighted_point((px10, p11z, p1y0), (6, 1, 2))
                    , weighted_point((px10, p11z, p1y0), (1, 6, 2))
                    , weighted_point((p01z, p11z, px11), (6, 1, 2))
                    , weighted_point((p01z, p11z, px11), (1, 6, 2))
                    ]
        t13 = torus20_from_points(wpoints13)

        # Add torus centered around f14 = Face(px10, p11z, p1y0)
        wpoints14 = [ weighted_point((px10, p11z, p01z), (6, 1, 2))
                    , weighted_point((px10, p11z, p01z), (1, 6, 2))
                    , weighted_point((px10, p1y0, px00), (6, 1, 2))
                    , weighted_point((px10, p1y0, px00), (1, 6, 2))
                    , weighted_point((p11z, p1y0, p1y1), (6, 1, 2))
                    , weighted_point((p11z, p1y0, p1y1), (1, 6, 2))
                    ]
        t14 = torus20_from_points(wpoints14)

        # Add torus centered around f15 = Face(p1y0, p11z, p1y1)
        wpoints15 = [ weighted_point((p1y0, p11z, px10), (6, 1, 2))
                    , weighted_point((p1y0, p11z, px10), (1, 6, 2))
                    , weighted_point((p1y0, p1y1, p10z), (6, 1, 2))
                    , weighted_point((p1y0, p1y1, p10z), (1, 6, 2))
                    , weighted_point((p11z, p1y1, px11), (6, 1, 2))
                    , weighted_point((p11z, p1y1, px11), (1, 6, 2))
                    ]
        t15 = torus20_from_points(wpoints15)

        # Add torus centered around f16 = Face(p1y1, p11z, px11)
        wpoints16 = [ weighted_point((p1y1, p11z, p1y0), (6, 1, 2))
                    , weighted_point((p1y1, p11z, p1y0), (1, 6, 2))
                    , weighted_point((p1y1, px11, px01), (6, 1, 2))
                    , weighted_point((p1y1, px11, px01), (1, 6, 2))
                    , weighted_point((p11z, px11, p01z), (6, 1, 2))
                    , weighted_point((p11z, px11, p01z), (1, 6, 2))
                    ]
        t16 = torus20_from_points(wpoints16)

        # Add torus centered around f17 = Face(p1y1, px11, px01)
        wpoints17 = [ weighted_point((p1y1, px11, p11z), (6, 1, 2))
                    , weighted_point((p1y1, px11, p11z), (1, 6, 2))
                    , weighted_point((p1y1, px01, p10z), (6, 1, 2))
                    , weighted_point((p1y1, px01, p10z), (1, 6, 2))
                    , weighted_point((px11, px01, p0y1), (6, 1, 2))
                    , weighted_point((px11, px01, p0y1), (1, 6, 2))
                    ]
        t17 = torus20_from_points(wpoints17)

        # Add torus centered around f18 = Face(px01, px11, p0y1)
        wpoints18 = [ weighted_point((px01, px11, p1y1), (6, 1, 2))
                    , weighted_point((px01, px11, p1y1), (1, 6, 2))
                    , weighted_point((px01, p0y1, p00z), (6, 1, 2))
                    , weighted_point((px01, p0y1, p00z), (1, 6, 2))
                    , weighted_point((px11, p0y1, p01z), (6, 1, 2))
                    , weighted_point((px11, p0y1, p01z), (1, 6, 2))
                    ]
        t18 = torus20_from_points(wpoints18)

        # Add torus centered around f19 = Face(p0y1, px11, p01z)
        wpoints19 = [ weighted_point((p0y1, px11, px01), (6, 1, 2))
                    , weighted_point((p0y1, px11, px01), (1, 6, 2))
                    , weighted_point((p0y1, p01z, p0y0), (6, 1, 2))
                    , weighted_point((p0y1, p01z, p0y0), (1, 6, 2))
                    , weighted_point((px11, p01z, p11z), (6, 1, 2))
                    , weighted_point((px11, p01z, p11z), (1, 6, 2))
                    ]
        t19 = torus20_from_points(wpoints19)

        # Add torus centered around f20 = Face(p01z, px11, p11z)
        wpoints20 = [ weighted_point((p01z, px11, p0y1), (6, 1, 2))
                    , weighted_point((p01z, px11, p0y1), (1, 6, 2))
                    , weighted_point((p01z, p11z, px10), (6, 1, 2))
                    , weighted_point((p01z, p11z, px10), (1, 6, 2))
                    , weighted_point((px11, p11z, p1y1), (6, 1, 2))
                    , weighted_point((px11, p11z, p1y1), (1, 6, 2))
                    ]
        t20 = torus20_from_points(wpoints20)

        self.tori20 = [  t1,  t2,  t3,  t4,  t5,  t6,  t7,  t8,  t9, t10
                      , t11, t12, t13, t14, t15, t16, t17, t18, t19, t20
                      ]

# def render_icosa_verts():
#    for v in icosa_verts:
#        mesh.primitive_ico_sphere_add(subdivisions=4, location=v.coordinates(), size= vertex_radius)

########################################
# Add planar hexagons
########################################
def torus20_from_points(points) -> Torus:
    return Torus(torus20_minor_radius, points)


def weight_4_5(center):
    return lambda other: (4 / 9) * center + (5 / 9) * other


def weighted_point(points3, weights3) -> Point:
    (p1, p2, p3) = points3
    (w1, w2, w3) = weights3
    weight_sum = w1 + w2 + w3
    weights = [w1/weight_sum, w2/weight_sum, w3/weight_sum]
    coords_x = [p1.x, p2.x, p3.x]
    coords_y = [p1.y, p2.y, p3.y]
    coords_z = [p1.z, p2.z, p3.z]
    def weighted(coords):
        return sum([w*c for (w,c) in zip(weights, coords)])
    return Point(weighted(coords_x), weighted(coords_y), weighted(coords_z))


def weighted_torus12(center, others):
    points = list(map(weight_4_5(center), others))
    return Torus(torus12_minor_radius, points)

def main():
    print('Hello, world!')
    orb = Orbicle()
    orb.print()

if __name__ == '__main__':
    main()
