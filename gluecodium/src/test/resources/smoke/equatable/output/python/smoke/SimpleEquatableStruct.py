

from __future__ import annotations

from smoke.NonEquatableClass import NonEquatableClass
from smoke.NonEquatableInterface import NonEquatableInterface


from _native_base import _NativeBase

import generated


class SimpleEquatableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SimpleEquatableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.SimpleEquatableStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def class_field(self) -> NonEquatableClass:
        """"""
        return NonEquatableClass(self._native.class_field)
    @class_field.setter
    def class_field(self, value: NonEquatableClass):
      self._native.class_field = getattr(value, "_native", value)



    @property
    def interface_field(self) -> NonEquatableInterface:
        """"""
        return NonEquatableInterface(self._native.interface_field)
    @interface_field.setter
    def interface_field(self, value: NonEquatableInterface):
      self._native.interface_field = getattr(value, "_native", value)



    @property
    def nullable_class_field(self):
        """"""
        return Optional[NonEquatableClass](self._native.nullable_class_field)
    @nullable_class_field.setter
    def nullable_class_field(self, value):
      self._native.nullable_class_field = getattr(value, "_native", value)



    @property
    def nullable_interface_field(self):
        """"""
        return Optional[NonEquatableInterface](self._native.nullable_interface_field)
    @nullable_interface_field.setter
    def nullable_interface_field(self, value):
      self._native.nullable_interface_field = getattr(value, "_native", value)


