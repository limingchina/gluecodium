

from smoke.Point import Point
from smoke.TestStruct import TestStruct
from smoke.float import float
from smoke.list[TestStruct] import list[TestStruct]

from _native_base import _NativeBase


class TypeDefs(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def method_with_primitive_type_def(self, input: float) -> float:
        """"""
        return self._native.method_with_primitive_type_def(input)


    def method_with_complex_type_def(self, input: list[TestStruct]) -> list[TestStruct]:
        """"""
        return self._native.method_with_complex_type_def(input)


    def return_nested_int_type_def(self, input: float) -> float:
        """"""
        return self._native.return_nested_int_type_def(input)


    def return_test_struct_type_def(self, input: TestStruct) -> TestStruct:
        """"""
        return self._native.return_test_struct_type_def(input)


    def return_nested_struct_type_def(self, input: TestStruct) -> TestStruct:
        """"""
        return self._native.return_nested_struct_type_def(input)


    def return_type_def_point_from_type_collection(self, input: Point) -> Point:
        """"""
        return self._native.return_type_def_point_from_type_collection(input)


    @property
    def primitive_type_property(self) -> list[float]:
        """"""
        return self._native.primitive_type_property


