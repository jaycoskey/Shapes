#!/usr/local/bin/python3.7

from math import (acos, sqrt)
from numpy import mean

from util import *

########################################
# Types
########################################
class Point(object):
    def __init__(self, x, y, z):
        self.x = eps(x)
        self.y = eps(y)
        self.z = eps(z)

    def __add__(self, other):
        return Point( self.x + other.x
                    , self.y + other.y
                    , self.z + other.z
                    )

    def __rmul__(self, other):
        return Point(other * self.x, other * self.y, other * self.z)

    def __str__(self):
        return '({0:>7.4g}, {1:>7.4g}, {2:>7.4g})'.format(self.x, self.y, self.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def coords(self):
        return self.x, self.y, self.z

    @property
    def distance_from(self):
        return lambda other: (self - other).norm

    @property
    def norm(self):
        return sqrt(self.norm2)

    @property
    def norm2(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2


class Vector(object):
    def __init__(self, x, y, z):
        self.x = eps(x)
        self.y = eps(y)
        self.z = eps(z)

    def __rmul__(self, other):
        return Vector(other * self.x, other * self.y, other * self.z)

    def __str__(self):
        return '({0:>7.4g}, {1:>7.4g}, {2:>7.4g})'.format(self.x, self.y, self.z)

    @property
    def norm(self):
        return sqrt(self.norm2)

    @property
    def norm2(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def cross(self, other):
        a = self
        b = other
        return Vector( a.y * b.z - a.z * b.y
                     , a.z * b.x - a.x * b.z
                     , a.x * b.y - a.y * b.x
                     )

    def dot(self, other):
        a = self
        b = other
        return a.x * b.x + a.y * b.y + a.z * b.z

    def normalized(self):
        nrm = self.norm
        return Vector(self.x / nrm, self.y / nrm, self.z / nrm) if (nrm > epsilon_threshold) \
               else Vector(0.0, 0.0, 0.0)


class Cylinder(object):
    def __init__(self, center1: Point, center2: Point, r: float):
        self.center1 = center1
        self.center2 = center2
        self.r = r

    def __str__(self):
        return 'Cylinder from {0:>7.4g} to {1:>7.4g} with r={2:>7.4g})'.format(
            self.center1, self.center2, self.r)


class Torus(object):
    def __init__(self, minor_radius, points):
        self.center       = average_point(points)
        self.minor_radius = minor_radius

        distances_from_center = [self.center.distance_from(p) for p in points]
        self.major_radius     = mean(distances_from_center)

        deltas      = [p - s        for (p,s)    in adjacent_pairs(points)]
        normals     = [d1.cross(d2) for (d1, d2) in adjacent_pairs(deltas)]
        self.normal = average_vector(normals).normalized()

    def __str__(self):
        return 'Torus: center={0}, normal={1}, R={2:>7.4f}, r={3:>7.4f}'.format(
            self.center, self.normal, self.major_radius, self.minor_radius)

class Triangle(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

def angle_between(vec1, vec2):
    dot_prod  = vec1.dot(vec2)
    norm_prod = vec1.norm * vec2.norm
    return acos(dot_prod / norm_prod)

# def average_point(*points):
#   center = Point()
#   for point in points:
#       center += point
#   center /= points.Length
def avg(items):
    num = len(items)
    x_coords = [p.x for p in items]
    y_coords = [p.y for p in items]
    z_coords = [p.z for p in items]
    sum_x = sum(x_coords)
    sum_y = sum(y_coords)
    sum_z = sum(z_coords)
    return sum_x/num, sum_y/num, sum_z/num

def average_point(points) -> Point:
    (val_x, val_y, val_z) = avg(points)
    return Point(val_x, val_y, val_z)

def average_vector(vectors) -> Vector:
    (val_x, val_y, val_z) = avg(vectors)
    return Vector(val_x, val_y, val_z)

def mk_cyl(center1, center2):
    return Cylinder(center1, center2, r = test_cube_edge_radius)

def main():
    print('Hello, world!')


if __name__ == '__main__':
    main()
