

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.ValidationUtilsValidation import ValidationUtilsValidation
from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode


from _native_base import _NativeBase

import generated


class StructsWithMethodsVector(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsWithMethodsVector):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsWithMethodsVector(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


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


    def distance_to(self, other: StructsWithMethodsVector) -> float:
        """"""
        return _wrap(self._native.distance_to(_unwrap(other, StructsWithMethodsVector)), float)

    def add(self, other: StructsWithMethodsVector) -> StructsWithMethodsVector:
        """"""
        return _wrap(self._native.add(_unwrap(other, StructsWithMethodsVector)), StructsWithMethodsVector)

    @staticmethod
    def validate(x: float, y: float) -> bool:
        """"""
        return generated.smoke_StructsWithMethodsVector.validate(_unwrap(x, float), _unwrap(y, float))

    @staticmethod
    def create(*args, **kwargs) -> StructsWithMethodsVector:
        """"""
        native_result = generated.smoke_StructsWithMethodsVector.create(*[_unwrap(a) for a in args])
        return StructsWithMethodsVector(native_result)



