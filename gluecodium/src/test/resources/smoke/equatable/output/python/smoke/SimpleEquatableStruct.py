

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated

from smoke.NonEquatableClass import NonEquatableClass
from smoke.NonEquatableInterface import NonEquatableInterface

class SimpleEquatableStruct(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_SimpleEquatableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_SimpleEquatableStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, __class__):
            return False
        return self._native.__gluecodium_equals__(other._native)

    __hash__ = None

    def as_key(self):
        """Return an isolated immutable value snapshot for dictionaries and sets."""
        return _struct_key(self, __class__)

    @property
    def class_field(self) -> NonEquatableClass:
        return _wrap(self._native.class_field, NonEquatableClass)
    @class_field.setter
    def class_field(self, value: NonEquatableClass):
      self._native.class_field = _unwrap(value, NonEquatableClass)


    @property
    def interface_field(self) -> NonEquatableInterface:
        return _wrap(self._native.interface_field, NonEquatableInterface)
    @interface_field.setter
    def interface_field(self, value: NonEquatableInterface):
      self._native.interface_field = _unwrap(value, NonEquatableInterface)


    @property
    def nullable_class_field(self):
        return _wrap(self._native.nullable_class_field, Optional[NonEquatableClass])
    @nullable_class_field.setter
    def nullable_class_field(self, value):
      self._native.nullable_class_field = _unwrap(value, Optional[NonEquatableClass])


    @property
    def nullable_interface_field(self):
        return _wrap(self._native.nullable_interface_field, Optional[NonEquatableInterface])
    @nullable_interface_field.setter
    def nullable_interface_field(self, value):
      self._native.nullable_interface_field = _unwrap(value, Optional[NonEquatableInterface])
