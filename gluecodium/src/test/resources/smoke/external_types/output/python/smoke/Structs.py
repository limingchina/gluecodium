

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class Structs(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def get_external_struct() -> Structs.ExternalStruct:
        native_result = generated.smoke_Structs.get_external_struct()
        return _get_or_create_wrapper(native_result, Structs.ExternalStruct)

    @staticmethod
    def get_another_external_struct() -> Structs.AnotherExternalStruct:
        native_result = generated.smoke_Structs.get_another_external_struct()
        return _get_or_create_wrapper(native_result, Structs.AnotherExternalStruct)

    class ExternalStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsExternalStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_StructsExternalStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def string_field(self) -> str:
            return _wrap(self._native.string_field, str)
        @string_field.setter
        def string_field(self, value: str):
          self._native.string_field = _unwrap(value, str)
    
    
        @property
        def external_string_field(self) -> str:
            return _wrap(self._native.external_string_field, str)
        @external_string_field.setter
        def external_string_field(self, value: str):
          self._native.external_string_field = _unwrap(value, str)
    
    
        @property
        def external_array_field(self) -> list[int]:
            return _wrap(self._native.external_array_field, list[int])
        @external_array_field.setter
        def external_array_field(self, value: list[int]):
          self._native.external_array_field = _unwrap(value, list[int])
    
    
        @property
        def external_struct_field(self) -> Structs.AnotherExternalStruct:
            return _wrap(self._native.external_struct_field, Structs.AnotherExternalStruct)
        @external_struct_field.setter
        def external_struct_field(self, value: Structs.AnotherExternalStruct):
          self._native.external_struct_field = _unwrap(value, Structs.AnotherExternalStruct)
    
    
    
    
    class AnotherExternalStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsAnotherExternalStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_StructsAnotherExternalStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def int_field(self) -> int:
            return _wrap(self._native.int_field, int)
        @int_field.setter
        def int_field(self, value: int):
          self._native.int_field = _unwrap(value, int)
    
    
    

