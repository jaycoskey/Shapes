#!/usr/local/bin/python3.7

# Goal: Visualize then 3D-print a particular sphere-like 3D shape.
#       The components are line segments (cylinders) and circles (toruses).

from enum import Flag, auto

import sys
sys.path.append('/home/jmc/Desktop/jmc_20220915/git/jaycoskey/Shapes/Orbicle')

from blend import *
from icosahedron import *
from scene import Scene


class OrbicleComponent(Flag):
    HexgridVerts = auto()
    HexgridEdges = auto()
    Tori12 = auto()
    Tori20 = auto()


class Orbicle(object):
    def __init__(self):
        self._icosa = Icosahedron()
        self.tori12 = self.get_tori12()
        self.tori20 = self.get_tori20()
        self.hexgrid_verts, self.hexgrid_edges = self.get_hexgrid()

    def get_hexgrid(self):
        hexgrid_verts = []
        hexgrid_edges = []

        # TODO: Refactor toward DRY
        for face in self._icosa.faces:
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
                    hexgrid_verts.append(v)
                for (v1, v2) in adjacent_pairs(hexagon):
                    hexgrid_edges.append(Cylinder(v1, v2, Config.hexgrid_edge_radius))

        return (hexgrid_verts, hexgrid_edges)

    def get_tori12(self):
        """Compute icosahedral-vertex-centered tori"""
        def weighted_t12(center, others):
            def weight_4_5(center):
                return lambda other: (4 / 9) * center + (5 / 9) * other

            points = list(map(weight_4_5(center), others))
            return Torus(Config.torus12_minor_radius, points)

        tori12 = [ weighted_t12(center=px00, others=[p00z, p10z, p1y0, px10, p0y0])
                 , weighted_t12(center=px01, others=[px11, p1y1, p10z, p00z, p0y1])
                 , weighted_t12(center=px10, others=[px00, p1y0, p11z, p01z, p0y0])
                 , weighted_t12(center=px11, others=[p11z, p1y1, px01, p0y1, p01z])
                 , weighted_t12(center=p0y0, others=[p0y1, p00z, px00, px10, p01z])
                 , weighted_t12(center=p0y1, others=[px11, px01, p00z, p0y0, p01z])
                 , weighted_t12(center=p1y0, others=[p1y1, p11z, px10, px00, p10z])
                 , weighted_t12(center=p1y1, others=[px11, p11z, p1y0, p10z, px01])
                 , weighted_t12(center=p00z, others=[px01, p10z, px00, p0y0, p0y1])
                 , weighted_t12(center=p01z, others=[px11, p0y1, p0y0, px10, p11z])
                 , weighted_t12(center=p10z, others=[px01, p1y1, p1y0, px00, p00z])
                 , weighted_t12(center=p11z, others=[p01z, px10, p1y0, p1y1, px11])
                 ]
        return tori12

    def get_tori20(self):
        def mk_t20(points) -> Torus:
            return Torus(Config.torus20_minor_radius, points)

        def get_weighted_points(pa, pb, pc, pd, pe, pf):
            return [ weighted_point((pa, pb, pd), (6, 1, 2))
                   , weighted_point((pa, pb, pd), (1, 6, 2))
                   , weighted_point((pa, pc, pe), (6, 1, 2))
                   , weighted_point((pa, pc, pe), (1, 6, 2))
                   , weighted_point((pb, pc, pf), (6, 1, 2))
                   , weighted_point((pb, pc, pf), (1, 6, 2))
                   ]


        """Compute icosahedral-face-centered tori"""
        # Add torus centered around f1  = Face(px00, p10z, p00z)
        wpoints1 = get_weighted_points(px00, p10z, p00z, p1y0, p0y0, px01)
        t1 = mk_t20(wpoints1)

        # Add torus centered around f2  = Face(px00, p00z, p0y0)
        wpoints2 = get_weighted_points(px00, p00z, p0y0, p10z, px10, p0y1)
        t2 = mk_t20(wpoints2)

        # Add torus centered around f3  = Face(px00, p0y0, px10)
        wpoints3 = get_weighted_points(px00, p0y0, px10, p00z, p1y0, p01z)
        t3 = mk_t20(wpoints3)

        # Add torus centered around f4  = Face(px00, px10, p1y0)
        wpoints4 = get_weighted_points(px00, px10, p1y0, p0y0, p10z, p11z)
        t4 = mk_t20(wpoints4)

        # Add torus centered around f5  = Face(px00, p1y0, p10z)
        wpoints5 = get_weighted_points(px00, p1y0, p10z, px10, p00z, p1y1)
        t5 = mk_t20(wpoints5)

        # Add torus centered around f6  = Face(p10z, p1y0, p1y1)
        wpoints6 = get_weighted_points(p10z, p1y0, p1y1, px00, px01, p11z)
        t6 = mk_t20(wpoints6)

        # Add torus centered around f7  = Face(p10z, p1y1, px01)
        wpoints7 = get_weighted_points(p10z, p1y1, px01, p1y0, p00z, px11)
        t7 = mk_t20(wpoints7)

        # Add torus centered around f8  = Face(p10z, px01, p00z)
        wpoints8 = get_weighted_points(p10z, px01, p00z, p1y1, px00, p0y1)
        t8 = mk_t20(wpoints8)

        # Add torus centered around f9  = Face(p00z, px01, p0y1)
        wpoints9 = get_weighted_points(p00z, px01, p0y1, p10z, p0y0, px11)
        t9 = mk_t20(wpoints9)

        # Add torus centered around f10 = Face(p00z, p0y1, p0y0)
        wpoints10 = get_weighted_points(p00z, p0y1, p0y0, px01, px00, p01z)
        t10 = mk_t20(wpoints10)

        # Add torus centered around f11 = Face(p0y0, p0y1, p01z)
        wpoints11 = get_weighted_points(p0y0, p0y1, p01z, p00z, px10, px11)
        t11 = mk_t20(wpoints11)

        # Add torus centered around f12 = Face(p0y0, p01z, px10)
        wpoints12 = get_weighted_points(p0y0, p01z, px10, p0y1, px00, p11z)
        t12 = mk_t20(wpoints12)

        # Add torus centered around f13 = Face(px10, p01z, p11z)
        wpoints13 = get_weighted_points(px10, p01z, p11z, p0y0, p1y0, px11)
        t13 = mk_t20(wpoints13)

        # Add torus centered around f14 = Face(px10, p11z, p1y0)
        wpoints14 = get_weighted_points(px10, p11z, p1y0, p01z, px00, p1y1)
        t14 = mk_t20(wpoints14)

        # Add torus centered around f15 = Face(p1y0, p11z, p1y1)
        wpoints15 = get_weighted_points(p1y0, p11z, p1y1, px10, p10z, px11)
        t15 = mk_t20(wpoints15)

        # Add torus centered around f16 = Face(p1y1, p11z, px11)
        wpoints16 = get_weighted_points(p1y1, p11z, px11, p1y0, px01, p01z)
        t16 = mk_t20(wpoints16)

        # Add torus centered around f17 = Face(p1y1, px11, px01)
        wpoints17 = get_weighted_points(p1y1, px11, px01, p11z, p10z, p0y1)
        t17 = mk_t20(wpoints17)

        # Add torus centered around f18 = Face(px01, px11, p0y1)
        wpoints18 = get_weighted_points(px01, px11, p0y1, p1y1, p00z, p01z)
        t18 = mk_t20(wpoints18)

        # Add torus centered around f19 = Face(p0y1, px11, p01z)
        wpoints19 = get_weighted_points(p0y1, px11, p01z, px01, p0y0, p11z)
        t19 = mk_t20(wpoints19)

        # Add torus centered around f20 = Face(p01z, px11, p11z)
        wpoints20 = get_weighted_points(p01z, px11, p11z, p0y1, px10, p1y1)
        t20 = mk_t20(wpoints20)

        tori20 = [  t1,  t2,  t3,  t4,  t5,  t6,  t7,  t8,  t9, t10
                 , t11, t12, t13, t14, t15, t16, t17, t18, t19, t20
                 ]
        return tori20

    # TODO: De-dupe vertices.
    def print(self):
        print('12 (smaller) vertex-centered tori')
        for t in self.tori12:
            print(t)
        print()
        print('20 (larger) face-centered tori')
        for t in self.tori20:
            print(t)
        #for hv in self.hexgrid_verts:
        #    print(hv)
        #for he in self.hexgrid_edges:
        #    print(he)

    def write_stl_file(self, stl_path=Config.path_stl, component_flags=None, verbose=False):
        verbose = True
        if verbose:
            print(f'Entering Orbicle.write_stl_file to write {stl_path}')
        if component_flags is None:
            cf_hv  = OrbicleComponent.HexgridVerts
            cf_he  = OrbicleComponent.HexgridEdges
            cf_t12 = OrbicleComponent.Tori12
            cf_t20 = OrbicleComponent.Tori20
            component_flags = cf_hv | cf_he | cf_t12 | cf_t20

        sys.stdout.flush()
        Scene.clear()
        # delete_all()
        if component_flags & OrbicleComponent.HexgridVerts:
            for hv in self.hexgrid_verts:
                hv.set_radius(Config.hexgrid_vertex_radius)
                hv.add_to_scene()
        if component_flags & OrbicleComponent.HexgridEdges:
            for he in self.hexgrid_edges:
                he.add_to_scene()
        if component_flags & OrbicleComponent.Tori12:
            for t in self.tori12:
                t.add_to_scene()
        if component_flags & OrbicleComponent.Tori20:
            for t in self.tori12:
                t.add_to_scene()
        Scene.write_stl_file(stl_path)

# ========================================
# Helping functions

# Used by both get_hexgrid and get_tori20()
def weighted_point(points, weights) -> Point3:
    def weighted(coords):
        return sum([w*c for (w,c) in zip(weights, coords)])

    # TODO: Use numpy transpose
    (p1, p2, p3) = points
    coords_x = [p1.x, p2.x, p3.x]
    coords_y = [p1.y, p2.y, p3.y]
    coords_z = [p1.z, p2.z, p3.z]
    return Point3(weighted(coords_x), weighted(coords_y), weighted(coords_z))

# ========================================
# Test functions

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
    Scene.write_stl_file('test_icosa_wireframe.stl')

# ========================================
def main():
    orb = Orbicle()
    orb.write_stl_file(Config.path_stl_hexgrid_verts, OrbicleComponent.HexgridVerts)
    orb.write_stl_file(Config.path_stl_hexgrid_edges, OrbicleComponent.HexgridEdges)
    orb.write_stl_file(Config.path_stl_tori12, OrbicleComponent.Tori12)
    orb.write_stl_file(Config.path_stl_tori20, OrbicleComponent.Tori20)

    if False:
        orb.write_stl_file(Config.path_stl, component_flags_all)


if __name__ == '__main__':
    main()
