

from smoke.ExampleStruct import ExampleStruct
from smoke.InternalErrorCode import InternalErrorCode
from smoke.PropertiesInterface import PropertiesInterface

from _native_base import _NativeBase


class Properties(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    @property
    def built_in_type_property(self) -> int:
        """"""
        return self._native.built_in_type_property



    @property
    def readonly_property(self) -> float:
        """"""
        return self._native.readonly_property



    @property
    def struct_property(self) -> ExampleStruct:
        """"""
        return self._native.struct_property



    @property
    def array_property(self) -> list[str]:
        """"""
        return self._native.array_property



    @property
    def complex_type_property(self) -> InternalErrorCode:
        """"""
        return self._native.complex_type_property



    @property
    def byte_buffer_property(self) -> bytes:
        """"""
        return self._native.byte_buffer_property



    @property
    def instance_property(self) -> PropertiesInterface:
        """"""
        return self._native.instance_property



    @property
    def is_boolean_property(self) -> bool:
        """"""
        return self._native.is_boolean_property



    @property
    def static_property(self) -> str:
        """"""
        return self._native.static_property



    @property
    def static_readonly_property(self) -> ExampleStruct:
        """"""
        return self._native.static_readonly_property


