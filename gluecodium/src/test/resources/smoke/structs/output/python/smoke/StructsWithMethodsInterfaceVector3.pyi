

from smoke.ValidationUtilsValidation import ValidationUtilsValidation
from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode
import typing


from _native_base import _NativeBase

import generated


class StructsWithMethodsInterfaceVector3(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsWithMethodsInterfaceVector3):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsWithMethodsInterfaceVector3(*[_unwrap(arg) for arg in args]))


    @property
    def x(self) -> float:
        """"""
        return _wrap(self._native.x, float)
    @x.setter
    def x(self, value: float):
      self._native.x = _unwrap(value, float)



    @property
    def y(self) -> float:
        """"""
        return _wrap(self._native.y, float)
    @y.setter
    def y(self, value: float):
      self._native.y = _unwrap(value, float)



    @property
    def z(self) -> float:
        """"""
        return _wrap(self._native.z, float)
    @z.setter
    def z(self, value: float):
      self._native.z = _unwrap(value, float)


    def distance_to(self, other: StructsWithMethodsInterfaceVector3) -> float: ...

    def add(self, other: StructsWithMethodsInterfaceVector3) -> StructsWithMethodsInterfaceVector3: ...

    @staticmethod
    def validate(x: float, y: float, z: float) -> bool: ...

    @typing.overload
    @staticmethod
    def create(input: str) -> StructsWithMethodsInterfaceVector3: ...

    @typing.overload
    @staticmethod
    def create(other: StructsWithMethodsInterfaceVector3) -> StructsWithMethodsInterfaceVector3: ...

