

from __future__ import annotations

from smoke.TypeCollectionPoint import TypeCollectionPoint
from smoke.TypeDefsTestStruct import TypeDefsTestStruct

from _native_base import _NativeBase

import generated


class TypeDefs(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def method_with_primitive_type_def(input: float) -> float:
        """"""
        return generated.TypeDefs.method_with_primitive_type_def(input)

    @staticmethod
    def method_with_complex_type_def(input: list[TypeDefsTestStruct]) -> list[TypeDefsTestStruct]:
        """"""
        return generated.TypeDefs.method_with_complex_type_def(input)

    @staticmethod
    def return_nested_int_type_def(input: float) -> float:
        """"""
        return generated.TypeDefs.return_nested_int_type_def(input)

    @staticmethod
    def return_test_struct_type_def(input: TypeDefsTestStruct) -> TypeDefsTestStruct:
        """"""
        native_result = generated.TypeDefs.return_test_struct_type_def(input._native)
        return TypeDefsTestStruct(native_result)

    @staticmethod
    def return_nested_struct_type_def(input: TypeDefsTestStruct) -> TypeDefsTestStruct:
        """"""
        native_result = generated.TypeDefs.return_nested_struct_type_def(input._native)
        return TypeDefsTestStruct(native_result)

    @staticmethod
    def return_type_def_point_from_type_collection(input: TypeCollectionPoint) -> TypeCollectionPoint:
        """"""
        native_result = generated.TypeDefs.return_type_def_point_from_type_collection(input._native)
        return TypeCollectionPoint(native_result)

    @property
    def primitive_type_property(self) -> list[float]:
        """"""
        return self._native.primitive_type_property

    @primitive_type_property.setter
    def primitive_type_property(self, value: list[float]):
        self._native.primitive_type_property = value

