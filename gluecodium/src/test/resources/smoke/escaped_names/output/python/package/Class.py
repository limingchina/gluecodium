

from __future__ import annotations

from package.Enum import Enum
from package.ExceptionError import ExceptionError
from package.Interface import Interface
from package.Struct import Struct
from package.list[Struct] import list[Struct]


from _native_base import _NativeBase

import generated


class Class(
    Interface)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def constructor() -> Class:
        """"""
        native_result = generated.Class.constructor()
        return Class(native_result)


    def fun(self, double: list[Struct]) -> Struct:
        """"""
        return self._native.fun(double._native)


    @property
    def property(self) -> Enum:
        """"""
        return self._native.property

    @property.setter
    def property(self, value: Enum):
        self._native.property = value

