

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.PropertiesInterface import PropertiesInterface

class Properties(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @property
    def built_in_type_property(self) -> int:
        return _wrap(self._native.built_in_type_property, int)

    @built_in_type_property.setter
    def built_in_type_property(self, value: int):
        self._native.built_in_type_property = _unwrap(value, int)

    @property
    def readonly_property(self) -> float:
        return _wrap(self._native.readonly_property, float)


    @property
    def struct_property(self) -> Properties.ExampleStruct:
        return _wrap(self._native.struct_property, Properties.ExampleStruct)

    @struct_property.setter
    def struct_property(self, value: Properties.ExampleStruct):
        self._native.struct_property = _unwrap(value, Properties.ExampleStruct)

    @property
    def array_property(self) -> list[str]:
        return _wrap(self._native.array_property, list[str])

    @array_property.setter
    def array_property(self, value: list[str]):
        self._native.array_property = _unwrap(value, list[str])

    @property
    def complex_type_property(self) -> Properties.InternalErrorCode:
        return _wrap(self._native.complex_type_property, Properties.InternalErrorCode)

    @complex_type_property.setter
    def complex_type_property(self, value: Properties.InternalErrorCode):
        self._native.complex_type_property = _unwrap(value, Properties.InternalErrorCode)

    @property
    def byte_buffer_property(self) -> bytes:
        return _wrap(self._native.byte_buffer_property, bytes)

    @byte_buffer_property.setter
    def byte_buffer_property(self, value: bytes):
        self._native.byte_buffer_property = _unwrap(value, bytes)

    @property
    def instance_property(self) -> PropertiesInterface:
        return _wrap(self._native.instance_property, PropertiesInterface)

    @instance_property.setter
    def instance_property(self, value: PropertiesInterface):
        self._native.instance_property = _unwrap(value, PropertiesInterface)

    @property
    def is_boolean_property(self) -> bool:
        return _wrap(self._native.is_boolean_property, bool)

    @is_boolean_property.setter
    def is_boolean_property(self, value: bool):
        self._native.is_boolean_property = _unwrap(value, bool)

    @staticmethod
    def static_property() -> str:
        return _wrap(generated.smoke_Properties.static_property(), str)

    @staticmethod
    def static_property_set(value: str):
        generated.smoke_Properties.static_property_set(_unwrap(value, str))

    @staticmethod
    def static_readonly_property() -> Properties.ExampleStruct:
        return _wrap(generated.smoke_Properties.static_readonly_property(), Properties.ExampleStruct)

    class ExampleStruct(_NativeBase):
        def __init__(self, *args, **kwargs):
            if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PropertiesExampleStruct):
                super().__init__(args[0])
            else:
                super().__init__(generated.smoke_PropertiesExampleStruct(
                    *[_unwrap(arg) for arg in args],
                    **{k: _unwrap(v) for k, v in kwargs.items()}
                ))
    
        @property
        def value(self) -> float:
            return _wrap(self._native.value, float)
        @value.setter
        def value(self, value: float):
          self._native.value = _unwrap(value, float)
    
    
    
    
    class InternalErrorCode(Enum):
    
        ERROR_NONE = generated.smoke_PropertiesInternalErrorCode.ERROR_NONE
        ERROR_FATAL = generated.smoke_PropertiesInternalErrorCode.ERROR_FATAL
    
        @property
        def _native(self):
            return self.value
    
    

