

from package.Enum import Enum
from package.ExceptionError import ExceptionError
from package.Interface import Interface
from package.typesstruct import typesstruct


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

    def fun(self, double: list[typesstruct]) -> typesstruct:
        """"""
        return self._native.fun(double)


    @property
    def property(self) -> Enum:
        """"""
        return self._native.property

    @property.setter
    def property(self, value: Enum):
        self._native.property = value

