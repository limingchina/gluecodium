

from smoke.TypeCollection import TypeCollection
from enum import Enum
import typing

class TypeDefs:

    @staticmethod
    def method_with_primitive_type_def(input: float) -> float:
        ...

    @staticmethod
    def method_with_complex_type_def(input: list[TypeDefs.TestStruct]) -> list[TypeDefs.TestStruct]:
        ...

    @staticmethod
    def return_nested_int_type_def(input: float) -> float:
        ...

    @staticmethod
    def return_test_struct_type_def(input: TypeDefs.TestStruct) -> TypeDefs.TestStruct:
        ...

    @staticmethod
    def return_nested_struct_type_def(input: TypeDefs.TestStruct) -> TypeDefs.TestStruct:
        ...

    @staticmethod
    def return_type_def_point_from_type_collection(input: TypeCollection.Point) -> TypeCollection.Point:
        ...

    @property
    def primitive_type_property(self) -> list[float]:
        ...

    @primitive_type_property.setter
    def primitive_type_property(self, value: list[float]) -> None:
        ...

    class StructHavingAliasFieldDefinedBelow:
    
        field: float
    
    
    
    class TestStruct:
    
        something: str
    
    
    
    NestedIntTypeDef = float
    
    
    
    PrimitiveTypeDef = float
    
    
    
    StructArray = list[TestStruct]
    
    
    
    ComplexTypeDef = list[TestStruct]
    
    
    
    TestStructTypeDef = TestStruct
    
    
    
    NestedStructTypeDef = TestStruct
    
    

