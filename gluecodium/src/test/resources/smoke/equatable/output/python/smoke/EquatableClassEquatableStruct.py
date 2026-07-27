

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.PointerEquatableClass import PointerEquatableClass


from _native_base import _NativeBase

import generated


class EquatableClassEquatableStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EquatableClassEquatableStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EquatableClassEquatableStruct(
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
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = _unwrap(value, int)



    @property
    def string_field(self) -> str:
        """"""
        return _wrap(self._native.string_field, str)
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = _unwrap(value, str)



    @property
    def nested_equatable_instance(self) -> EquatableClass:
        """"""
        from smoke.EquatableClass import EquatableClass
        return _wrap(self._native.nested_equatable_instance, EquatableClass)
    @nested_equatable_instance.setter
    def nested_equatable_instance(self, value: EquatableClass):
      self._native.nested_equatable_instance = _unwrap(value, EquatableClass)



    @property
    def nested_pointer_equatable_instance(self) -> PointerEquatableClass:
        """"""
        return _wrap(self._native.nested_pointer_equatable_instance, PointerEquatableClass)
    @nested_pointer_equatable_instance.setter
    def nested_pointer_equatable_instance(self, value: PointerEquatableClass):
      self._native.nested_pointer_equatable_instance = _unwrap(value, PointerEquatableClass)


