#!/usr/local/bin/python3.7

import bpy


class Scene:
    @staticmethod
    def clear():
        for item in bpy.data.objects:
            bpy.data.objects.remove(item, do_unlink=True)
        for item in bpy.data.meshes:
            bpy.data.meshes.remove(item, do_unlink=True)

    @staticmethod
    def write_stl_file(stl_path):
        bpy.ops.export_mesh.stl(
            filepath=stl_path
            , check_existing=True
            , ascii=False
            # , apply_modifiers=True
            )
