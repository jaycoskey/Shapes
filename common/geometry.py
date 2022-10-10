#!/usr/local/bin/python3.7

from abc import ABC
from functools import reduce
from math import acos, fabs, sqrt
from mathutils import Quaternion
from numpy import mean
import operator
import os
import sys


import bpy


EPSILON = 10e-6


class Shape(ABC):
    def add_to_scene(self):
        raise NotImplementedError('Shape.add_to_scene')


class Cylinder(Shape):
    @staticmethod
    def make(center1, center2):
        return Cylinder(center1, center2, r=test_cube_edge_radius)

    def __init__(self, center1, center2, r):
        self.center1 = center1
        self.center2 = center2
        self.r = r

    def __str__(self):
        return 'Cylinder from {0:>7.4g} to {1:>7.4g} with r={2:>7.4g})'.format(
            self.center1, self.center2, self.r)

    def add_to_scene(self):
        loc          = Point3.avg([self.center1, self.center2])
        zunit        = Vec3(0, 0, 1)
        cylinder_dir = 0.5 * (self.center2 - self.center1)
        euler_rot    = Vec3.vectors2euler(zunit, cylinder_dir)
        bpy.ops.mesh.primitive_cylinder_add(
            vertices         = 32
            , radius         = self.r
            , depth          = (self.center2 - self.center1).norm()
            # , cap_ends=False
            , align='WORLD'
            , enter_editmode = False
            , location       = (loc.x, loc.y, loc.z)
            , rotation       = (euler_rot.x, euler_rot.y, euler_rot.z)
            # layers
            )


class Point3(Shape):
    @staticmethod
    def avg(ps):
        # print(f'Point3.avg(): ps[0] is a {type(ps[0])}')
        return Vec3.avg([p.as_vec3() for p in ps]).as_point3()

    def __init__(self, x, y, z):
        def eps(x):
            return 0.0 if fabs(x) < EPSILON else x
        self.x = eps(x)
        self.y = eps(y)
        self.z = eps(z)
        self.radius = None

    def __add__(self, other):
        return Point3( self.x + other.x
                    , self.y + other.y
                    , self.z + other.z
                    )

    def __rmul__(self, other):
        return Point3(other * self.x, other * self.y, other * self.z)

    def __str__(self):
        return '({0:>7.4g}, {1:>7.4g}, {2:>7.4g})'.format(self.x, self.y, self.z)

    def __sub__(self, other):
        other_type = type(other).__name__
        result_coords = (self.x - other.x, self.y - other.y, self.z - other.z)
        if other_type == 'Point3':
            return Vec3(*result_coords)
        elif other_type == 'Vec3':
            return Point3(*result_coords)
        else:
            assert(False)

    def add_to_scene(self, r=0.1):
        bpy.ops.mesh.primitive_ico_sphere_add(
            subdivisions=3
            , radius=r
            , align='WORLD'
            , enter_editmode=False
            , location=(self.x, self.y, self.z)
            # rotation=(0.0, 0.0, 0.0)  # Not needed
            # layers
            )

    def as_vec3(self):
        return Vec3(self.x, self.y, self.z)

    def coords(self):
        return self.x, self.y, self.z

    def distance_to(self, other):
        return (other - self).norm()

    def norm(self):
        return sqrt(self.norm2())

    def norm2(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def set_radius(self, r):
        self.radius = r


class Torus(Shape):
    def __init__(self, minor_radius, points):
        # adjacent_pairs([1,2,3,4,5]) returns [(1,2), (2,3), (3,4), (4,5), (5,1)]
        def adjacent_pairs(lst):
            list2 = list(lst)
            list2.append(list2.pop(0))
            return zip(lst, list2)

        self.center       = Point3.avg(points)
        self.minor_radius = minor_radius

        distances_to_center = [self.center.distance_to(p) for p in points]
        self.major_radius   = mean(distances_to_center)

        deltas      = [b - a        for (a, b)   in adjacent_pairs(points)]
        normals     = [d1.cross(d2) for (d1, d2) in adjacent_pairs(deltas)]
        self.normal = Vec3.avg(normals).normalized()

    def __str__(self):
        return 'Torus: center={0}, normal={1}, R={2:>7.4f}, r={3:>7.4f}'.format(
            self.center, self.normal, self.major_radius, self.minor_radius)

    def add_to_scene(self):
        zunit   = Vec3(0, 0, 1)
        euler_rot = Vec3.vectors2euler(zunit, self.normal)
        bpy.ops.mesh.primitive_torus_add(
            major_radius=self.major_radius
            , minor_radius=self.minor_radius
            , major_segments=48
            , minor_segments=12
            # , use_abso=False
            , abso_major_rad=1.0
            , abso_minor_rad=0.5
            , align='WORLD'
            , location=(self.center.x, self.center.y, self.center.z)
            , rotation=(euler_rot.x, euler_rot.y, euler_rot.z)
            )


class Triangle(Shape):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


class Vec3():
    @staticmethod
    def avg(vs):
        total = reduce(operator.add, vs, Vec3(0.0, 0.0, 0.0))
        count = len(vs)
        return total / count

    @staticmethod
    def vectors2euler(vec_ref, vec_actual):
        rot_axis  = vec_ref.cross(vec_actual).normalized()
        rot_angle = vec_actual.angle_to(vec_ref)
        quat_rot  = Quaternion((rot_axis.x, rot_axis.y, rot_axis.z), rot_angle)
        euler_rot = quat_rot.to_euler()
        return euler_rot

    def __init__(self, x, y, z):
        def eps(x):
            return 0.0 if fabs(x) < EPSILON else x
        self.x = eps(x)
        self.y = eps(y)
        self.z = eps(z)

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __neg__(self):
        return Vec3(-1.0 * self.x, -1.0 * self.y, -1.0 * self.z)

    def __rmul__(self, other):
        return Vec3(other * self.x, other * self.y, other * self.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self):
        return '({0:>7.4g}, {1:>7.4g}, {2:>7.4g})'.format(self.x, self.y, self.z)

    def __truediv__(self, denom):
        return Vec3(self.x / denom, self.y / denom, self.z / denom)

    def angle_to(self, other):
        # print(f'Vec3.angle_to(): self={self}, other={other}')
        dot_prod  = self.dot(other)
        norm_prod = self.norm() * other.norm()
        return acos(dot_prod / norm_prod)

    def as_point3(self):
        return Point3(self.x, self.y, self.z)

    def as_tuple(self):
        return (self.x, self.y, self.z)

    def cross(self, other):
        a = self
        b = other
        return Vec3( a.y * b.z - a.z * b.y
                   , a.z * b.x - a.x * b.z
                   , a.x * b.y - a.y * b.x
                   )

    def dot(self, other):
        a = self
        b = other
        return a.x * b.x + a.y * b.y + a.z * b.z

    def norm(self):
        return sqrt(self.norm2())

    def norm2(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def normalized(self):
        norm = self.norm()
        if norm > EPSILON:
            return Vec3(self.x / norm, self.y / norm, self.z / norm)
        else:
            return Vec3(0.0, 0.0, 0.0)


