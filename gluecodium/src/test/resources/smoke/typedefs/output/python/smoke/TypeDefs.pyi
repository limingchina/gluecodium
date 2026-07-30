

from smoke.TypeCollectionPoint import TypeCollectionPoint
from smoke.TypeDefsTestStruct import TypeDefsTestStruct
import typing

class TypeDefs:

    @staticmethod
    def method_with_primitive_type_def(input: float) -> float:
        ...

    @staticmethod
    def method_with_complex_type_def(input: list[TypeDefsTestStruct]) -> list[TypeDefsTestStruct]:
        ...

    @staticmethod
    def return_nested_int_type_def(input: float) -> float:
        ...

    @staticmethod
    def return_test_struct_type_def(input: TypeDefsTestStruct) -> TypeDefsTestStruct:
        ...

    @staticmethod
    def return_nested_struct_type_def(input: TypeDefsTestStruct) -> TypeDefsTestStruct:
        ...

    @staticmethod
    def return_type_def_point_from_type_collection(input: TypeCollectionPoint) -> TypeCollectionPoint:
        ...

    @property
    def primitive_type_property(self) -> list[float]:
        ...

    @primitive_type_property.setter
    def primitive_type_property(self, value: list[float]) -> None:
        ...

