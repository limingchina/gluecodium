

from smoke.StructsAllTypesStruct import StructsAllTypesStruct
from smoke.StructsNestingImmutableStruct import StructsNestingImmutableStruct
from smoke.StructsPoint import StructsPoint
from smoke.TypeCollectionAllTypesStruct import TypeCollectionAllTypesStruct
from smoke.TypeCollectionPoint import TypeCollectionPoint
import typing

class Structs:

    @staticmethod
    def swap_point_coordinates(input: StructsPoint) -> StructsPoint:
        ...

    @staticmethod
    def return_all_types_struct(input: StructsAllTypesStruct) -> StructsAllTypesStruct:
        ...

    @staticmethod
    def create_point(x: float, y: float) -> TypeCollectionPoint:
        ...

    @staticmethod
    def modify_all_types_struct(input: TypeCollectionAllTypesStruct) -> TypeCollectionAllTypesStruct:
        ...

