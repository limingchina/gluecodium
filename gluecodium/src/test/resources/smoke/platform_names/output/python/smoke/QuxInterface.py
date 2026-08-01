

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.QuxTypes import QuxTypes

class QuxInterface(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def qux_method(self, qux_parameter: str) -> QuxTypes.QuxStruct:
        return _wrap(self._native.qux_method(_unwrap(qux_parameter, str)), QuxTypes.QuxStruct)

    @staticmethod
    def qux_create(make_parameter: str) -> QuxInterface:
        native_result = generated.smoke_QuxInterface.qux_create(_unwrap(make_parameter, str))
        return _get_or_create_wrapper(native_result, QuxInterface)

    @property
    def qux_property(self) -> int:
        return _wrap(self._native.qux_property, int)

    @qux_property.setter
    def qux_property(self, value: int):
        self._native.qux_property = _unwrap(value, int)


