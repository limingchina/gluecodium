

from smoke.NonEquatableClass import NonEquatableClass
from smoke.NonEquatableInterface import NonEquatableInterface
import typing


from _native_base import _NativeBase

import generated


class SimpleEquatableStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SimpleEquatableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.SimpleEquatableStruct(*[_unwrap(arg) for arg in args]))


    @property
    def class_field(self) -> NonEquatableClass:
        """"""
        return _wrap(self._native.class_field, NonEquatableClass)
    @class_field.setter
    def class_field(self, value: NonEquatableClass):
      self._native.class_field = _unwrap(value, NonEquatableClass)



    @property
    def interface_field(self) -> NonEquatableInterface:
        """"""
        return _wrap(self._native.interface_field, NonEquatableInterface)
    @interface_field.setter
    def interface_field(self, value: NonEquatableInterface):
      self._native.interface_field = _unwrap(value, NonEquatableInterface)



    @property
    def nullable_class_field(self):
        """"""
        return _wrap(self._native.nullable_class_field, Optional[NonEquatableClass])
    @nullable_class_field.setter
    def nullable_class_field(self, value):
      self._native.nullable_class_field = _unwrap(value, Optional[NonEquatableClass])



    @property
    def nullable_interface_field(self):
        """"""
        return _wrap(self._native.nullable_interface_field, Optional[NonEquatableInterface])
    @nullable_interface_field.setter
    def nullable_interface_field(self, value):
      self._native.nullable_interface_field = _unwrap(value, Optional[NonEquatableInterface])


