

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class FieldCustomConstructorsMix(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_FieldCustomConstructorsMix):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_FieldCustomConstructorsMix(*[_unwrap(arg) for arg in args]))


    @property
    def string_field(self) -> str:
        """"""
        return _wrap(self._native.string_field, str)
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = _unwrap(value, str)



    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = _unwrap(value, int)



    @property
    def bool_field(self) -> bool:
        """"""
        return _wrap(self._native.bool_field, bool)
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = _unwrap(value, bool)


    @staticmethod
    def create_me(int_value: int, dummy: float) -> FieldCustomConstructorsMix:
        """"""
        native_result = generated.smoke_FieldCustomConstructorsMix.create_me(_unwrap(int_value, int), _unwrap(dummy, float))
        return FieldCustomConstructorsMix(native_result)

