

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

