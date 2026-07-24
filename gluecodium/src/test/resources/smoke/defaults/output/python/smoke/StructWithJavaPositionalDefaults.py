

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class StructWithJavaPositionalDefaults(_NativeBase):
    """Foo Bar this is a comment"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructWithJavaPositionalDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithJavaPositionalDefaults(*[_unwrap(arg) for arg in args]))

    first init!
    @property
    def first_init_field(self) -> int:
        """first init!"""
        return _wrap(self._native.first_init_field, int)
    @first_init_field.setter
    def first_init_field(self, value: int):
      self._native.first_init_field = _unwrap(value, int)


    first free!
    @property
    def first_free_field(self) -> str:
        """first free!"""
        return _wrap(self._native.first_free_field, str)
    @first_free_field.setter
    def first_free_field(self, value: str):
      self._native.first_free_field = _unwrap(value, str)


    second init yeah!
    @property
    def second_init_field(self) -> float:
        """second init yeah!"""
        return _wrap(self._native.second_init_field, float)
    @second_init_field.setter
    def second_init_field(self, value: float):
      self._native.second_init_field = _unwrap(value, float)


    second free here!
    @property
    def second_free_field(self) -> bool:
        """second free here!"""
        return _wrap(self._native.second_free_field, bool)
    @second_free_field.setter
    def second_free_field(self, value: bool):
      self._native.second_free_field = _unwrap(value, bool)


    third should be last!
    @property
    def third_init_field(self) -> str:
        """third should be last!"""
        return _wrap(self._native.third_init_field, str)
    @third_init_field.setter
    def third_init_field(self, value: str):
      self._native.third_init_field = _unwrap(value, str)


