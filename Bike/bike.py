#!/usr/local/bin/python3.7

from enum import Flag, auto
from math import cos, pi, sin
from mathutils import Quaternion
import os
import sys

import bpy

sys.path.append(os.path.dirname(__file__) + '/../common/')
from geometry import Cylinder, Point3, Torus, Vec3
from scene import Scene


p3_ORIGIN = Point3(0.0, 0.0, 0.0)

v3_ZERO = Vec3(0.0, 0.0, 0.0)
v3_XHAT = Vec3(1.0, 0.0, 0.0)
v3_YHAT = Vec3(0.0, 1.0, 0.0)
v3_ZHAT = Vec3(0.0, 0.0, 1.0)


class BikeComponent(Flag):
    Axle = auto()
    Chain = auto()
    Frame = auto()
    Gear = auto()
    Pedal = auto()
    Seat = auto()
    Shock = auto()
    Steering = auto()
    Wheel = auto()


class ComponentBase:
    """Spatially locatable (vec3 + rot3) and renderable base class
    Note: self.origin_offset is only determined at construction.
          If the base object is later moved, this object does not also automatically move.
    """
    def __init__(self, parent=None, parent_offset=v3_ZERO):
        self.parent = parent
        self.parent_offset = parent_offset
        self.shapes = None

    def offset() -> Vec3:
        return (parent.offset() if parent else v3_ZERO) + parent_offset

    def add_to_scene(self):
        for shape in self.shapes:
            shape.add_to_scene()


class BikeConfig:
    # Use terms to identify Rubik's cube faces
    frame_down  =   0.0 * v3_ZHAT  # Z-: distance below origin
    frame_up    =  18.0 * v3_ZHAT  # Z+: distance above origin
    frame_back  = -24.0 * v3_XHAT  # X-: distance behind origin
    frame_front =  70.0 * v3_XHAT  # X+: distance forward of origin
    frame_left  =  33.0 * v3_YHAT  # Y+: distance left of origin
    frame_right = -33.0 * v3_YHAT  # Y-: distance right of origin

    frame_radius = 1.0

    pedal1l_offset = Vec3(1.0,  1.5, -0.25)
    pedal1r_offset = Vec3(1.0,  0.5, -0.25)
    pedal2l_offset = Vec3(1.0, -0.5, -0.25)
    pedal2r_offset = Vec3(1.0, -1.5, -0.25)

    seat1_offset = Vec3(0.0,  1.0, 0.5)
    seat2_offset = Vec3(0.0, -1.0, 0.5)

    wheel_offset_back =   v3_ZERO
    wheel_offset_front =  60.0 * v3_XHAT
    wheel_offset_left =   40.0 * v3_YHAT
    wheel_offset_right = -40.0 * v3_YHAT
    wheel_major_radius= 9.0
    wheel_minor_radius= 3.0
    wheel_major_segments = 48
    wheel_minor_segments = 12


# Using MathWorks' Automated Driving Toolbox coordinate system: X=long, Y=lat(left), Z=vertical
class Bike():
    def __init__(self):
        Cfg = BikeConfig

        # ===== Add frame =====
        self.frame = Frame()

        # ===== Add pedals =====
        self.pedal_1l = Pedal(self.frame, Cfg.pedal1l_offset)
        self.pedal_1r = Pedal(self.frame, Cfg.pedal1r_offset)
        self.pedal_2l = Pedal(self.frame, Cfg.pedal2l_offset)
        self.pedal_2r = Pedal(self.frame, Cfg.pedal2r_offset)

        # ===== Add seats =====
        self.seat_1 = Seat(self.frame, Cfg.seat1_offset)
        self.seat_2 = Seat(self.frame, Cfg.seat2_offset)

        # ===== Add steering =====
        # TODO: Add steering

        # ===== Add wheels =====
        wheel_offset_fl =  Cfg.wheel_offset_front + Cfg.wheel_offset_left
        wheel_offset_fr =  Cfg.wheel_offset_front + Cfg.wheel_offset_right
        wheel_offset_bl = -Cfg.wheel_offset_back  + Cfg.wheel_offset_left
        wheel_offset_br = -Cfg.wheel_offset_back  + Cfg.wheel_offset_right

        # Wheels: fl=front left, br=back right, etc.
        self.wheel_fl = Wheel(self.frame, wheel_offset_fl,
                                 Cfg.wheel_major_radius, Cfg.wheel_minor_radius)
        self.wheel_fr = Wheel(self.frame, wheel_offset_fr,
                                 Cfg.wheel_major_radius, Cfg.wheel_minor_radius)
        self.wheel_bl = Wheel(self.frame, wheel_offset_bl,
                                 Cfg.wheel_major_radius,  Cfg.wheel_minor_radius)
        self.wheel_br = Wheel(self.frame, wheel_offset_br,
                                 Cfg.wheel_major_radius,  Cfg.wheel_minor_radius)

        self.axle_front = Axle(self.frame, Cfg.wheel_offset_front, 40, 2)
        self.axle_rear = Axle(self.frame, Cfg.wheel_offset_back, 40, 2)

        # ===== Add chains and shock absorbers =====
        # TODO: Add chains
        # TODO: Add shocks

    def write_stl_file(self, stl_path, component_flags=None):
        def add_if_is_component(name, obj, prefix):
            if (name == prefix) or ('_' in name and name.split('_')[0].startswith(prefix)):
                if isinstance(obj, ComponentBase):
                    obj.add_to_scene()
                elif isinstance(obj, list):
                    for item in obj:
                        if isinstance(item, ComponentBase):
                            item.add_to_scene()

        if component_flags is None:
            component_flags = BikeComponent.Frame
            component_flags |= BikeComponent.Axle
            # component_flags |= BikeComponent.Chain
            # component_flags |= BikeComponent.Gear
            # component_flags |= BikeComponent.Pedal
            # component_flags |= BikeComponent.Seat
            # component_flags |= BikeComponent.Shock
            # component_flags |= BikeComponent.Steering
            component_flags |= BikeComponent.Wheel

        for name, prop in self.__dict__.items():
            # print(f'\tHandling property {name}')

            if component_flags & BikeComponent.Axle:
                add_if_is_component(name, prop, 'axle')
            if component_flags & BikeComponent.Chain:
                add_if_is_component(name, prop, 'chain')
            if component_flags & BikeComponent.Frame:
                add_if_is_component(name, prop, 'frame')
            if component_flags & BikeComponent.Gear:
                add_if_is_component(name, prop, 'gear')
            if component_flags & BikeComponent.Pedal:
                add_if_is_component(name, prop, 'pedal')
            if component_flags & BikeComponent.Seat:
                add_if_is_component(name, prop, 'seat')
            if component_flags & BikeComponent.Shock:
                add_if_is_component(name, prop, 'shock')
            if component_flags & BikeComponent.Steering:
                add_if_is_component(name, prop, 'steering')
            if component_flags & BikeComponent.Wheel:
                add_if_is_component(name, prop, 'wheel')

        bpy.ops.export_mesh.stl(filepath=stl_path, check_existing=True, ascii=False)  # apply_modifiers=True

# ========================================

# Offset is at the center of the back axle
# The Frame has various "sockets": intended offsets of different components
class Frame(ComponentBase):
    def __init__(self):
        self.parent = None
        # self.parent_offset = BikeConfig.wheel_major_radius_back * v3_ZHAT
        self.origin = p3_ORIGIN + BikeConfig.wheel_major_radius * v3_ZHAT
        self.shapes = self.get_shapes(self.origin)

    def add_to_scene(self):
        for shape in self.shapes:
            shape.add_to_scene()

    def get_shapes(self, origin):
        def mk_frame_cylinder(p1, p2):
            return Cylinder(origin + p1, origin + p2, Cfg.frame_radius)

        result = []
        Cfg = BikeConfig
        # Reference vectors
        v3_flu = Cfg.frame_front + Cfg.frame_left  + Cfg.frame_up
        v3_fld = Cfg.frame_front + Cfg.frame_left  + Cfg.frame_down
        v3_fru = Cfg.frame_front + Cfg.frame_right + Cfg.frame_up
        v3_frd = Cfg.frame_front + Cfg.frame_right + Cfg.frame_down

        v3_blu = Cfg.frame_back  + Cfg.frame_left  + 2 * Cfg.frame_up
        v3_bld = Cfg.frame_back  + Cfg.frame_left  + Cfg.frame_down
        v3_bru = Cfg.frame_back  + Cfg.frame_right + 2 * Cfg.frame_up
        v3_brd = Cfg.frame_back  + Cfg.frame_right + Cfg.frame_down

        # == Front face ==

        # == Back face ==
        back_face = [ mk_frame_cylinder(v3_blu, v3_bru)  # Back-up     rail
                    , mk_frame_cylinder(v3_bld, v3_brd)  # Back-down   rail
                    , mk_frame_cylinder(v3_blu, v3_bld)  # Back-left   pillar
                    , mk_frame_cylinder(v3_bru, v3_brd)  # Back-right  pillar
                    ]

        # == Left foot-rail ==
        cyls_left = [ mk_frame_cylinder(v3_fld, v3_bld) ]

        # == Right foot-rail ==
        cyls_right = [ mk_frame_cylinder(v3_frd, v3_brd) ]

        # == Wheel supports ==
        ws_front = Cfg.wheel_offset_front
        ws_back = 0.5 * Cfg.frame_back
        ws_up = 0.5 * Cfg.frame_up

        ws_fl_bd = Cfg.frame_left + ws_front + ws_back
        ws_fl_bu = Cfg.frame_left + ws_front + ws_back + ws_up
        ws_fl_fd = Cfg.frame_left + ws_front - ws_back
        ws_fl_fu = Cfg.frame_left + ws_front - ws_back + ws_up

        ws_fr_bd = Cfg.frame_right + ws_front + ws_back
        ws_fr_bu = Cfg.frame_right + ws_front + ws_back + ws_up
        ws_fr_fd = Cfg.frame_right + ws_front - ws_back
        ws_fr_fu = Cfg.frame_right + ws_front - ws_back + ws_up

        ws_bl_bd = Cfg.frame_left + ws_back
        ws_bl_bu = Cfg.frame_left + ws_back + ws_up
        ws_bl_fd = Cfg.frame_left - ws_back
        ws_bl_fu = Cfg.frame_left - ws_back + ws_up

        ws_br_bd = Cfg.frame_right + ws_back
        ws_br_bu = Cfg.frame_right + ws_back + ws_up
        ws_br_fd = Cfg.frame_right - ws_back
        ws_br_fu = Cfg.frame_right - ws_back + ws_up

        wsupport_front = [
            # Front portion
            mk_frame_cylinder(ws_fl_fd, ws_fr_fd),
            mk_frame_cylinder(ws_fl_fu, ws_fr_fu),

            mk_frame_cylinder(ws_fl_fd, ws_fl_fu),
            mk_frame_cylinder(ws_fr_fd, ws_fr_fu),

            # Back portion
            mk_frame_cylinder(ws_fl_bd, ws_fr_bd),
            mk_frame_cylinder(ws_fl_bu, ws_fr_bu),

            mk_frame_cylinder(ws_fl_bd, ws_fl_bu),
            mk_frame_cylinder(ws_fr_bd, ws_fr_bu),

            # Top portion
            mk_frame_cylinder(ws_fl_fu, ws_fl_bu),
            mk_frame_cylinder(ws_fr_fu, ws_fr_bu),
            ]

        wsupport_back = [
            # Front portion
            mk_frame_cylinder(ws_bl_fd, ws_br_fd),
            mk_frame_cylinder(ws_bl_fu, ws_br_fu),

            mk_frame_cylinder(ws_bl_fd, ws_bl_fu),
            mk_frame_cylinder(ws_br_fd, ws_br_fu),

            # Back portion
            mk_frame_cylinder(ws_bl_bd, ws_br_bd),
            mk_frame_cylinder(ws_bl_bu, ws_br_bu),

            mk_frame_cylinder(ws_bl_bd, ws_bl_bu),
            mk_frame_cylinder(ws_br_bd, ws_br_bu),

            # Top portion
            mk_frame_cylinder(ws_bl_fu, ws_bl_bu),
            mk_frame_cylinder(ws_br_fu, ws_br_bu),
            ]

        # == Center supports ==
        csupport_center = [
            mk_frame_cylinder(-ws_back, ws_front + ws_back),
            mk_frame_cylinder(-ws_back + ws_up, ws_front + ws_back + ws_up)
            ]

        csupport_sides = [
            mk_frame_cylinder(ws_bl_fu, ws_fl_bu),
            mk_frame_cylinder(ws_br_fu, ws_fr_bu)
            ]

        # == Back shelf ==
        back_shelf = [
            mk_frame_cylinder(Cfg.frame_left + ws_back + ws_up, Cfg.frame_left  + Cfg.frame_back + ws_up),
            mk_frame_cylinder(Cfg.frame_right + ws_back + ws_up, Cfg.frame_right  + Cfg.frame_back + ws_up)
        ]

        result = back_face + cyls_left + cyls_right + wsupport_front + wsupport_back + csupport_center + csupport_sides + back_shelf
        return result

# ========================================

class Axle(ComponentBase):
    def __init__(self, parent, parent_offset: Vec3, width, minor_radius):
        self.parent = parent
        self.parent_offset = parent_offset
        self.origin = self.parent.origin + parent_offset
        self.width = width
        self.minor_radius = minor_radius
        self.shapes = self.get_shapes(self.origin, self.width, self.minor_radius)

    def get_shapes(self, origin, width, minor_radius):
        return [Cylinder(origin + width * v3_YHAT, origin - width * v3_YHAT, minor_radius)]

class Chain(ComponentBase):
    def __init__(self, parent, parent_offset: Vec3):
        self.parent = parent
        self.parent_offset = parent_offset
        offset = self.parent.origin + parent_offset
        self.shapes = self.get_shapes(offset)

    def get_shapes(self, offset):
        raise NotImplementedError()

class Gear(ComponentBase):
    def __init__(self, parent, parent_offset: Vec3):
        self.parent = parent
        self.parent_offset = parent_offset
        self.origin = self.parent.origin() + parent_offset
        # self.shapes = self.get_shapes(self.origin)

    def get_shapes(self, origin):
        raise NotImplementedError()


class Pedal(ComponentBase):
    """Default orientation is for left pedal. For right, use angle=180 degrees, vertical axis (zhat)"""
    def __init__(self, parent, parent_offset: Vec3):
        self.parent = parent
        self.parent_offset = parent_offset
        self.origin = self.parent.origin + parent_offset
        # self.shapes = self.get_shapes(self.origin)

    def get_shapes(self, origin):
        raise NotImplementedError()


class Seat(ComponentBase):
    def __init__(self, parent, parent_offset: Vec3):
        self.parent = parent
        self.parent_offset = parent_offset
        self.origin = self.parent.origin + parent_offset
        # self.shapes = self.get_shapes(self.origin)

    def get_shapes(self, origin):
        raise NotImplementedError()


class Shock(ComponentBase):
    def __init__(self, parent, parent_offset: Vec3):
        self.parent = parent
        self.parent_offset = parent_offset
        self.origin = self.parent.origin + parent_offset
        # self.shapes = self.get_shapes(self.origin)

    def get_shapes(self, origin):
        raise NotImplementedError()


class Steering(ComponentBase):
    def __init__(self, parent, parent_offset: Vec3):
        self.parent = parent
        self.parent_offset = parent_offset
        self.origin = self.parent.origin + parent_offset
        # self.shapes = self.get_shapes(self.origin)

    def get_shapes(self, origin):
        raise NotImplementedError()


# By default, the wheel lies in the X-Z plane, so it has a latitudinal axis of rotation.
# TODO: Add spokes
class Wheel(ComponentBase):
    """Default orientation is in the X-Z plane"""
    def __init__(self, parent, parent_offset: Vec3, major_radius, minor_radius):
        self.parent = parent
        self.parent_offset: Vec3 = parent_offset
        self.origin: Point3 = self.parent.origin + parent_offset

        self.major_radius = major_radius
        self.minor_radius = minor_radius
        self.wheel_major_segments = BikeConfig.wheel_major_segments
        self.wheel_minor_segments = BikeConfig.wheel_minor_segments

        self.shapes = self.get_shapes(self.origin)

    def get_shapes(self, origin):
        def get_xz_spoke_points(radius, n):
            return [((origin + (radius * cos(angle) * v3_XHAT)) + (radius * sin(angle) * v3_ZHAT))
                       for angle in [pi/180 * degrees for degrees in range(0, 360, round(360/n))]
                       ]

        def get_xz_wheel_points(radius):
            return [origin + radius * v3_XHAT, origin + radius * v3_ZHAT, origin - radius * v3_XHAT, origin - radius * v3_ZHAT]

        major =  self.major_radius
        minor =  self.minor_radius
        spokes = [ Cylinder(origin, spoke_endpoint, 0.5) for spoke_endpoint in  get_xz_spoke_points(major, 8)]
        wheel = Torus(self.minor_radius, get_xz_wheel_points(self.major_radius))
        shapes = [ wheel ] + spokes
        return shapes


if __name__ == '__main__':
    bike = Bike()
    Scene.clear()
    bike.write_stl_file('bike.stl')
