

from smoke.QuxStruct import QuxStruct
import typing

from _native_base import _NativeBase

import generated


class QuxInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def qux_method(self, qux_parameter: str) -> QuxStruct: ...

    @staticmethod
    def qux_create(make_parameter: str) -> QuxInterface: ...

    @property
    def qux_property(self) -> int:
        """"""
        return _wrap(self._native.qux_property, int)

    @qux_property.setter
    def qux_property(self, value: int):
        self._native.qux_property = _unwrap(value, int)

