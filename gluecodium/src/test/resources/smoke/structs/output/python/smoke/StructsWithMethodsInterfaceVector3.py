

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.ValidationUtilsValidation import ValidationUtilsValidation
from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode


from _native_base import _NativeBase

import generated


class StructsWithMethodsInterfaceVector3(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_StructsWithMethodsInterfaceVector3):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsWithMethodsInterfaceVector3(*[_unwrap(arg) for arg in args]))


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


    def distance_to(self, other: StructsWithMethodsInterfaceVector3) -> float:
        """"""
        return _wrap(self._native.distance_to(_unwrap(other, StructsWithMethodsInterfaceVector3)), float)

    def add(self, other: StructsWithMethodsInterfaceVector3) -> StructsWithMethodsInterfaceVector3:
        """"""
        return _wrap(self._native.add(_unwrap(other, StructsWithMethodsInterfaceVector3)), StructsWithMethodsInterfaceVector3)

    @staticmethod
    def validate(x: float, y: float, z: float) -> bool:
        """"""
        return generated.smoke_StructsWithMethodsInterfaceVector3.validate(_unwrap(x, float), _unwrap(y, float), _unwrap(z, float))

    @staticmethod
    def create(*args, **kwargs) -> StructsWithMethodsInterfaceVector3:
        """"""
        native_result = generated.smoke_StructsWithMethodsInterfaceVector3.create(*[_unwrap(a) for a in args])
        return StructsWithMethodsInterfaceVector3(native_result)


