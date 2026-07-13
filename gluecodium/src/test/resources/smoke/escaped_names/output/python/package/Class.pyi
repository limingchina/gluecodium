

from package.Class import Class
from package.Enum import Enum
from package.ExceptionError import ExceptionError
from package.Interface import Interface
from package.Struct import Struct
from package.list[Struct] import list[Struct]

from _native_base import _NativeBase


class Class(
    Interface)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def constructor(self) -> Class:
        """"""
        return self._native.constructor()


    def fun(self, double: list[Struct]) -> Struct:
        """"""
        return self._native.fun(double)


    @property
    def property(self) -> Enum:
        """"""
        return self._native.property


