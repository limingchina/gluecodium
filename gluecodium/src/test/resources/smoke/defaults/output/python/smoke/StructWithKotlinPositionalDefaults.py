

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class StructWithKotlinPositionalDefaults(_NativeBase):
    """This is an important struct that uses positional default annotation."""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_StructWithKotlinPositionalDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructWithKotlinPositionalDefaults(*[_unwrap(arg) for arg in args]))


    @property
    def first_init_field(self) -> int:
        """"""
        return _wrap(self._native.first_init_field, int)
    @first_init_field.setter
    def first_init_field(self, value: int):
      self._native.first_init_field = _unwrap(value, int)



    @property
    def first_free_field(self) -> str:
        """"""
        return _wrap(self._native.first_free_field, str)
    @first_free_field.setter
    def first_free_field(self, value: str):
      self._native.first_free_field = _unwrap(value, str)



    @property
    def second_init_field(self) -> float:
        """"""
        return _wrap(self._native.second_init_field, float)
    @second_init_field.setter
    def second_init_field(self, value: float):
      self._native.second_init_field = _unwrap(value, float)



    @property
    def second_free_field(self) -> bool:
        """"""
        return _wrap(self._native.second_free_field, bool)
    @second_free_field.setter
    def second_free_field(self, value: bool):
      self._native.second_free_field = _unwrap(value, bool)



    @property
    def third_init_field(self) -> str:
        """"""
        return _wrap(self._native.third_init_field, str)
    @third_init_field.setter
    def third_init_field(self, value: str):
      self._native.third_init_field = _unwrap(value, str)


