

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.NonEquatableClass import NonEquatableClass
from smoke.NonEquatableInterface import NonEquatableInterface


from _native_base import _NativeBase

import generated


class SimpleEquatableStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_SimpleEquatableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_SimpleEquatableStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self._native == other._native

    def __hash__(self) -> int:
        return hash(self._native)


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


