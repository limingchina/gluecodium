

from smoke.ValidationUtilsValidation import ValidationUtilsValidation
from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode
import typing


from _native_base import _NativeBase

import generated


class StructsWithMethodsVector(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_StructsWithMethodsVector):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsWithMethodsVector(*[_unwrap(arg) for arg in args]))


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


    def distance_to(self, other: StructsWithMethodsVector) -> float: ...

    def add(self, other: StructsWithMethodsVector) -> StructsWithMethodsVector: ...

    @staticmethod
    def validate(x: float, y: float) -> bool: ...

    @typing.overload
    @staticmethod
    def create(x: float, y: float) -> StructsWithMethodsVector: ...

    @typing.overload
    @staticmethod
    def create(other: StructsWithMethodsVector) -> StructsWithMethodsVector: ...

    @typing.overload
    @staticmethod
    def create(input: int) -> StructsWithMethodsVector: ...

