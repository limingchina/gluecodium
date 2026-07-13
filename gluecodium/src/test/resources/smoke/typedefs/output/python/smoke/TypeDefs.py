

from __future__ import annotations

from smoke.Point import Point
from smoke.TestStruct import TestStruct
from smoke.float import float
from smoke.list[TestStruct] import list[TestStruct]


from _native_base import _NativeBase

import generated


class TypeDefs(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def method_with_primitive_type_def(input: float) -> float:
        """"""
        native_result = generated.TypeDefs.method_with_primitive_type_def(input)
        return float(native_result)

    @staticmethod

    def method_with_complex_type_def(input: list[TestStruct]) -> list[TestStruct]:
        """"""
        native_result = generated.TypeDefs.method_with_complex_type_def(input)
        return list[TestStruct](native_result)

    @staticmethod

    def return_nested_int_type_def(input: float) -> float:
        """"""
        native_result = generated.TypeDefs.return_nested_int_type_def(input)
        return float(native_result)

    @staticmethod

    def return_test_struct_type_def(input: TestStruct) -> TestStruct:
        """"""
        native_result = generated.TypeDefs.return_test_struct_type_def(input)
        return TestStruct(native_result)

    @staticmethod

    def return_nested_struct_type_def(input: TestStruct) -> TestStruct:
        """"""
        native_result = generated.TypeDefs.return_nested_struct_type_def(input)
        return TestStruct(native_result)

    @staticmethod

    def return_type_def_point_from_type_collection(input: Point) -> Point:
        """"""
        native_result = generated.TypeDefs.return_type_def_point_from_type_collection(input)
        return Point(native_result)


    @property
    def primitive_type_property(self) -> list[float]:
        """"""
        return self._native.primitive_type_property

    @primitive_type_property.setter
    def primitive_type_property(self, value: list[float]):
        self._native.primitive_type_property = value

