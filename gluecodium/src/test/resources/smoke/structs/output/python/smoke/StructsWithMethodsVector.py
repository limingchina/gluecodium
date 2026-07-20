

from __future__ import annotations

from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode


from _native_base import _NativeBase

import generated


class StructsWithMethodsVector(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsWithMethodsVector):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsWithMethodsVector(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def x(self) -> float:
        """"""
        return self._native.x
    @x.setter
    def x(self, value: float):
      self._native.x = getattr(value, "_native", value)



    @property
    def y(self) -> float:
        """"""
        return self._native.y
    @y.setter
    def y(self, value: float):
      self._native.y = getattr(value, "_native", value)


    def distance_to(self, other: StructsWithMethodsVector) -> float:
        """"""
        return self._native.distance_to(other._native)

    def add(self, other: StructsWithMethodsVector) -> StructsWithMethodsVector:
        """"""
        return self._native.add(other._native)

    @staticmethod
    def validate(x: float, y: float) -> bool:
        """"""
        return generated.StructsWithMethodsVector.validate(x, y)

    @staticmethod
    def create(*args, **kwargs) -> StructsWithMethodsVector:
        """"""
        native_result = generated.StructsWithMethodsVector.create(*[getattr(a, "_native", a) for a in args])
        return StructsWithMethodsVector(native_result)



