

from smoke.AllTypesStruct import AllTypesStruct
from smoke.NestingImmutableStruct import NestingImmutableStruct
from smoke.Point import Point
from smoke.list[AllTypesStruct] import list[AllTypesStruct]

class Structs:
    """"""

    def __init__(self, native):
        self._native = native


    def swap_point_coordinates(self, input: Point) -> Point:
        """"""
        return self._native.swap_point_coordinates(input)


    def return_all_types_struct(self, input: AllTypesStruct) -> AllTypesStruct:
        """"""
        return self._native.return_all_types_struct(input)


    def create_point(self, x: float, y: float) -> Point:
        """"""
        return self._native.create_point(x, y)


    def modify_all_types_struct(self, input: AllTypesStruct) -> AllTypesStruct:
        """"""
        return self._native.modify_all_types_struct(input)

