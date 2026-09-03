

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from fire.Enum1 import Enum1
from fire.Enum2 import Enum2
from fire.Enum3 import Enum3
from fire.Enum4 import Enum4

class EnumCollectionDefaults(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_EnumCollectionDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_EnumCollectionDefaults(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def list_field(self) -> list[Enum1]:
        return _wrap(self._native.list_field, list[Enum1])
    @list_field.setter
    def list_field(self, value: list[Enum1]):
      self._native.list_field = _unwrap(value, list[Enum1])


    @property
    def set_field(self) -> set[Enum2]:
        return _wrap(self._native.set_field, set[Enum2])
    @set_field.setter
    def set_field(self, value: set[Enum2]):
      self._native.set_field = _unwrap(value, set[Enum2])


    @property
    def map_field(self) -> dict[Enum3, Enum4]:
        return _wrap(self._native.map_field, dict[Enum3, Enum4])
    @map_field.setter
    def map_field(self, value: dict[Enum3, Enum4]):
      self._native.map_field = _unwrap(value, dict[Enum3, Enum4])



