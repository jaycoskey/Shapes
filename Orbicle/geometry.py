#!/bin/python

from math import *


########################################
# Types
########################################
class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point( self.x + other.x
                    , self.y + other.y
                    , self.z + other.z
                    )

    def __rmul__(self, other):
        return Point(other * self.x, other * self.y, other * self.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

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


# class LineSegment(object):
#     def __init__(self, end1: Point, end2: Point):
#         """
#         :type end1: Point
#         :type end2: Point
#         """
#         self.end1 = end1
#         self.end2 = end2


class Cylinder(object):
    def __init__(self, center1: Point, center2: Point, r: float):
        """
        :type center1: Point
        :type center2: Point
        :type r: float
        """
        self.center1 = center1
        self.center2 = center2
        self.r = r


class Torus(object):
    def __init__(self, minor_radius, points):
        self.center       = average(points)
        self.minor_radius = minor_radius
        self.major_radius = average(map(self.center.distance_from, points))


class Triangle(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


# def average(*points):
#   center = Point()
#   for point in points:
#       center += point
#   center /= points.Length
def average(points) -> Point:
    """
    :rtype: Point
    """
    num   = len(list(points))
    sum_x = sum(map(lambda p: p.x, points))
    sum_y = sum(map(lambda p: p.y, points))
    sum_z = sum(map(lambda p: p.z, points))
    assert isinstance(num, object)
    return Point(sum_x / num, sum_y / num, sum_z / num)


def main():
    print('Hello, world!')


if __name__ == '__main__':
    main()
