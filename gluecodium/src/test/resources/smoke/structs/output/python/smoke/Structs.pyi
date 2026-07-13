

from smoke.AllTypesStruct import AllTypesStruct
from smoke.NestingImmutableStruct import NestingImmutableStruct
from smoke.Point import Point
from smoke.list[AllTypesStruct] import list[AllTypesStruct]


from _native_base import _NativeBase

import generated


class Structs(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def swap_point_coordinates(input: Point) -> Point:
        """"""
        native_result = generated.Structs.swap_point_coordinates(input)
        return Point(native_result)

    @staticmethod

    def return_all_types_struct(input: AllTypesStruct) -> AllTypesStruct:
        """"""
        native_result = generated.Structs.return_all_types_struct(input)
        return AllTypesStruct(native_result)

    @staticmethod

    def create_point(x: float, y: float) -> Point:
        """"""
        native_result = generated.Structs.create_point(x, y)
        return Point(native_result)

    @staticmethod

    def modify_all_types_struct(input: AllTypesStruct) -> AllTypesStruct:
        """"""
        native_result = generated.Structs.modify_all_types_struct(input)
        return AllTypesStruct(native_result)

