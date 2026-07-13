

from __future__ import annotations

from smoke.ExampleStruct import ExampleStruct
from smoke.InternalErrorCode import InternalErrorCode
from smoke.PropertiesInterface import PropertiesInterface


from _native_base import _NativeBase

import generated


class Properties(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def built_in_type_property(self) -> int:
        """"""
        return self._native.built_in_type_property

    @built_in_type_property.setter
    def built_in_type_property(self, value: int):
        self._native.built_in_type_property = value


    @property
    def readonly_property(self) -> float:
        """"""
        return self._native.readonly_property



    @property
    def struct_property(self) -> ExampleStruct:
        """"""
        return self._native.struct_property

    @struct_property.setter
    def struct_property(self, value: ExampleStruct):
        self._native.struct_property = value


    @property
    def array_property(self) -> list[str]:
        """"""
        return self._native.array_property

    @array_property.setter
    def array_property(self, value: list[str]):
        self._native.array_property = value


    @property
    def complex_type_property(self) -> InternalErrorCode:
        """"""
        return self._native.complex_type_property

    @complex_type_property.setter
    def complex_type_property(self, value: InternalErrorCode):
        self._native.complex_type_property = value


    @property
    def byte_buffer_property(self) -> bytes:
        """"""
        return self._native.byte_buffer_property

    @byte_buffer_property.setter
    def byte_buffer_property(self, value: bytes):
        self._native.byte_buffer_property = value


    @property
    def instance_property(self) -> PropertiesInterface:
        """"""
        return self._native.instance_property

    @instance_property.setter
    def instance_property(self, value: PropertiesInterface):
        self._native.instance_property = value


    @property
    def is_boolean_property(self) -> bool:
        """"""
        return self._native.is_boolean_property

    @is_boolean_property.setter
    def is_boolean_property(self, value: bool):
        self._native.is_boolean_property = value


    @property
    def static_property(self) -> str:
        """"""
        return self._native.static_property

    @static_property.setter
    def static_property(self, value: str):
        self._native.static_property = value


    @property
    def static_readonly_property(self) -> ExampleStruct:
        """"""
        return self._native.static_readonly_property


from enum import Enum


class InternalErrorCode(Enum):
    """"""

    ERROR_NONE = 0
    ERROR_FATAL = 1

