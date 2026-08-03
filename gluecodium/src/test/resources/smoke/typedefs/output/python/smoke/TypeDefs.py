

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.TypeCollection import TypeCollection

class TypeDefs(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def method_with_primitive_type_def(input: float) -> float:
        return generated.smoke_TypeDefs.method_with_primitive_type_def(_unwrap(input, float))

    @staticmethod
    def method_with_complex_type_def(input: list[TypeDefs.TestStruct]) -> list[TypeDefs.TestStruct]:
        return _wrap(generated.smoke_TypeDefs.method_with_complex_type_def(_unwrap(input, list[TypeDefs.TestStruct])), list[TypeDefs.TestStruct])

    @staticmethod
    def return_nested_int_type_def(input: float) -> float:
        return generated.smoke_TypeDefs.return_nested_int_type_def(_unwrap(input, float))

    @staticmethod
    def return_test_struct_type_def(input: TypeDefs.TestStruct) -> TypeDefs.TestStruct:
        native_result = generated.smoke_TypeDefs.return_test_struct_type_def(_unwrap(input, TypeDefs.TestStruct))
        return _get_or_create_wrapper(native_result, TypeDefs.TestStruct)

    @staticmethod
    def return_nested_struct_type_def(input: TypeDefs.TestStruct) -> TypeDefs.TestStruct:
        native_result = generated.smoke_TypeDefs.return_nested_struct_type_def(_unwrap(input, TypeDefs.TestStruct))
        return _get_or_create_wrapper(native_result, TypeDefs.TestStruct)

    @staticmethod
    def return_type_def_point_from_type_collection(input: TypeCollection.Point) -> TypeCollection.Point:
        native_result = generated.smoke_TypeDefs.return_type_def_point_from_type_collection(_unwrap(input, TypeCollection.Point))
        return _get_or_create_wrapper(native_result, TypeCollection.Point)

    @property
    def primitive_type_property(self) -> list[float]:
        return _wrap(self._native.primitive_type_property, list[float])

    @primitive_type_property.setter
    def primitive_type_property(self, value: list[float]):
        self._native.primitive_type_property = _unwrap(value, list[float])

    class StructHavingAliasFieldDefinedBelow(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypeDefsStructHavingAliasFieldDefinedBelow):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypeDefsStructHavingAliasFieldDefinedBelow(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def field(self) -> float:
            return _wrap(self._native.field, float)
        @field.setter
        def field(self, value: float):
          self._native.field = _unwrap(value, float)
    
    
    
    
    class TestStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_TypeDefsTestStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_TypeDefsTestStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def something(self) -> str:
            return _wrap(self._native.something, str)
        @something.setter
        def something(self, value: str):
          self._native.something = _unwrap(value, str)
    
    
    
    
    NestedIntTypeDef = float
    
    
    
    PrimitiveTypeDef = float
    
    
    
    StructArray = list[TestStruct]
    
    
    
    ComplexTypeDef = list[TestStruct]
    
    
    
    TestStructTypeDef = TestStruct
    
    
    
    NestedStructTypeDef = TestStruct
    
    

