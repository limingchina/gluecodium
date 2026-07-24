

from smoke.PublicClassInternalStruct import PublicClassInternalStruct
import typing

from _native_base import _NativeBase

import generated


class PublicClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def internal_method(self, input: PublicClassInternalStruct) -> PublicClassInternalStruct: ...

    @property
    def internal_struct_property(self) -> PublicClassInternalStruct:
        """"""
        return _wrap(self._native.internal_struct_property, PublicClassInternalStruct)

    @internal_struct_property.setter
    def internal_struct_property(self, value: PublicClassInternalStruct):
        self._native.internal_struct_property = _unwrap(value, PublicClassInternalStruct)

