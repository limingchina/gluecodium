

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class StructWithCollectionDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructWithCollectionDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithCollectionDefaults(*[_unwrap(arg) for arg in args]))


    @property
    def empty_list_field(self) -> list[str]:
        """"""
        return _wrap(self._native.empty_list_field, list[str])
    @empty_list_field.setter
    def empty_list_field(self, value: list[str]):
      self._native.empty_list_field = _unwrap(value, list[str])



    @property
    def empty_map_field(self) -> dict[str, str]:
        """"""
        return _wrap(self._native.empty_map_field, dict[str, str])
    @empty_map_field.setter
    def empty_map_field(self, value: dict[str, str]):
      self._native.empty_map_field = _unwrap(value, dict[str, str])



    @property
    def empty_set_field(self) -> set[str]:
        """"""
        return _wrap(self._native.empty_set_field, set[str])
    @empty_set_field.setter
    def empty_set_field(self, value: set[str]):
      self._native.empty_set_field = _unwrap(value, set[str])



    @property
    def list_field(self) -> list[str]:
        """"""
        return _wrap(self._native.list_field, list[str])
    @list_field.setter
    def list_field(self, value: list[str]):
      self._native.list_field = _unwrap(value, list[str])



    @property
    def map_field(self) -> dict[str, str]:
        """"""
        return _wrap(self._native.map_field, dict[str, str])
    @map_field.setter
    def map_field(self, value: dict[str, str]):
      self._native.map_field = _unwrap(value, dict[str, str])



    @property
    def set_field(self) -> set[str]:
        """"""
        return _wrap(self._native.set_field, set[str])
    @set_field.setter
    def set_field(self, value: set[str]):
      self._native.set_field = _unwrap(value, set[str])


