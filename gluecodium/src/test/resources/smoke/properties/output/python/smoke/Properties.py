

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.PropertiesExampleStruct import PropertiesExampleStruct
from smoke.PropertiesInterface import PropertiesInterface
from smoke.PropertiesInternalErrorCode import PropertiesInternalErrorCode

from _native_base import _NativeBase

import generated


class Properties(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @property
    def built_in_type_property(self) -> int:
        """"""
        return _wrap(self._native.built_in_type_property, int)

    @built_in_type_property.setter
    def built_in_type_property(self, value: int):
        self._native.built_in_type_property = _unwrap(value, int)

    @property
    def readonly_property(self) -> float:
        """"""
        return _wrap(self._native.readonly_property, float)


    @property
    def struct_property(self) -> PropertiesExampleStruct:
        """"""
        return _wrap(self._native.struct_property, PropertiesExampleStruct)

    @struct_property.setter
    def struct_property(self, value: PropertiesExampleStruct):
        self._native.struct_property = _unwrap(value, PropertiesExampleStruct)

    @property
    def array_property(self) -> list[str]:
        """"""
        return _wrap(self._native.array_property, list[str])

    @array_property.setter
    def array_property(self, value: list[str]):
        self._native.array_property = _unwrap(value, list[str])

    @property
    def complex_type_property(self) -> PropertiesInternalErrorCode:
        """"""
        return _wrap(self._native.complex_type_property, PropertiesInternalErrorCode)

    @complex_type_property.setter
    def complex_type_property(self, value: PropertiesInternalErrorCode):
        self._native.complex_type_property = _unwrap(value, PropertiesInternalErrorCode)

    @property
    def byte_buffer_property(self) -> bytes:
        """"""
        return _wrap(self._native.byte_buffer_property, bytes)

    @byte_buffer_property.setter
    def byte_buffer_property(self, value: bytes):
        self._native.byte_buffer_property = _unwrap(value, bytes)

    @property
    def instance_property(self) -> PropertiesInterface:
        """"""
        return _wrap(self._native.instance_property, PropertiesInterface)

    @instance_property.setter
    def instance_property(self, value: PropertiesInterface):
        self._native.instance_property = _unwrap(value, PropertiesInterface)

    @property
    def is_boolean_property(self) -> bool:
        """"""
        return _wrap(self._native.is_boolean_property, bool)

    @is_boolean_property.setter
    def is_boolean_property(self, value: bool):
        self._native.is_boolean_property = _unwrap(value, bool)


    @staticmethod
    def static_property() -> str:
        """"""
        return _wrap(generated.smoke_Properties.static_property(), str)

    @staticmethod
    def static_property_set(value: str):
        generated.smoke_Properties.static_property_set(_unwrap(value, str))


    @staticmethod
    def static_readonly_property() -> PropertiesExampleStruct:
        """"""
        return _wrap(generated.smoke_Properties.static_readonly_property(), PropertiesExampleStruct)

