

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.StructsAllTypesStruct import StructsAllTypesStruct
from smoke.StructsNestingImmutableStruct import StructsNestingImmutableStruct
from smoke.StructsPoint import StructsPoint
from smoke.TypeCollectionAllTypesStruct import TypeCollectionAllTypesStruct
from smoke.TypeCollectionPoint import TypeCollectionPoint

from _native_base import _NativeBase

import generated


class Structs(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def swap_point_coordinates(input: StructsPoint) -> StructsPoint:
        native_result = generated.smoke_Structs.swap_point_coordinates(_unwrap(input, StructsPoint))
        return _get_or_create_wrapper(native_result, StructsPoint)

    @staticmethod
    def return_all_types_struct(input: StructsAllTypesStruct) -> StructsAllTypesStruct:
        native_result = generated.smoke_Structs.return_all_types_struct(_unwrap(input, StructsAllTypesStruct))
        return _get_or_create_wrapper(native_result, StructsAllTypesStruct)

    @staticmethod
    def create_point(x: float, y: float) -> TypeCollectionPoint:
        native_result = generated.smoke_Structs.create_point(_unwrap(x, float), _unwrap(y, float))
        return _get_or_create_wrapper(native_result, TypeCollectionPoint)

    @staticmethod
    def modify_all_types_struct(input: TypeCollectionAllTypesStruct) -> TypeCollectionAllTypesStruct:
        native_result = generated.smoke_Structs.modify_all_types_struct(_unwrap(input, TypeCollectionAllTypesStruct))
        return _get_or_create_wrapper(native_result, TypeCollectionAllTypesStruct)

