

from __future__ import annotations

from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode


from _native_base import _NativeBase

import generated


class StructsWithMethodsInterfaceVector3(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsWithMethodsInterfaceVector3):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsWithMethodsInterfaceVector3(*[getattr(arg, "_native", arg) for arg in args]))


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



    @property
    def z(self) -> float:
        """"""
        return self._native.z
    @z.setter
    def z(self, value: float):
      self._native.z = getattr(value, "_native", value)


    def distance_to(self, other: StructsWithMethodsInterfaceVector3) -> float:
        """"""
        return self._native.distance_to(other._native)

    def add(self, other: StructsWithMethodsInterfaceVector3) -> StructsWithMethodsInterfaceVector3:
        """"""
        return self._native.add(other._native)

    @staticmethod
    def validate(x: float, y: float, z: float) -> bool:
        """"""
        return generated.StructsWithMethodsInterfaceVector3.validate(x, y, z)

    @staticmethod
    def create(*args, **kwargs) -> StructsWithMethodsInterfaceVector3:
        """"""
        native_result = generated.StructsWithMethodsInterfaceVector3.create(*[getattr(a, "_native", a) for a in args])
        return StructsWithMethodsInterfaceVector3(native_result)


