

from package.Class import Class
from package.Enum import Enum
from package.ExceptionError import ExceptionError
from package.Interface import Interface
from package.Struct import Struct
from package.list[Struct] import list[Struct]

class Class(
    Interface):
    """"""

    def __init__(self, native):
        self._native = native


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


