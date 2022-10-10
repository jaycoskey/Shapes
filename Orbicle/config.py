#!/usr/local/bin/python3.7

class Config:
    epsilon_threshold     = 0.0001
    scale_factor          = 1.7

    hexgrid_edge_radius   = scale_factor * 0.03
    hexgrid_vertex_radius = scale_factor * 0.05

    torus_major_segments  = 90
    torus_minor_segments  = 18

    torus12_minor_radius  = scale_factor * 0.04
    torus20_minor_radius  = scale_factor * 0.04

    path_stl = 'orbicle.stl'
    path_stl_tori12 = 'orbicle_tori12.stl'
    path_stl_tori20 = 'orbicle_tori20.stl'
    path_stl_hexgrid_edges = 'orbicle_hexgrid_edges.stl'
    path_stl_hexgrid_verts = 'orbicle_hexgrid_verts.stl'

    # ========================================
    # Test parameters

    test_cube_edge_radius    = scale_factor * 0.05
    test_cube_vertex_radius  = scale_factor * 0.15

    test_icosa_edge_radius   = scale_factor * 0.05
    test_icosa_vertex_radius = scale_factor * 0.15
