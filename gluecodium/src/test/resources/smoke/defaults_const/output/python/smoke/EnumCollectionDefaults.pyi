

from fire.Enum1 import Enum1
from fire.Enum2 import Enum2
from fire.Enum3 import Enum3
from fire.Enum4 import Enum4
import typing


from _native_base import _NativeBase

import generated


class EnumCollectionDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumCollectionDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumCollectionDefaults(*[_unwrap(arg) for arg in args]))


    @property
    def list_field(self) -> list[Enum1]:
        """"""
        return _wrap(self._native.list_field, list[Enum1])
    @list_field.setter
    def list_field(self, value: list[Enum1]):
      self._native.list_field = _unwrap(value, list[Enum1])



    @property
    def set_field(self) -> set[Enum2]:
        """"""
        return _wrap(self._native.set_field, set[Enum2])
    @set_field.setter
    def set_field(self, value: set[Enum2]):
      self._native.set_field = _unwrap(value, set[Enum2])



    @property
    def map_field(self) -> dict[Enum3, Enum4]:
        """"""
        return _wrap(self._native.map_field, dict[Enum3, Enum4])
    @map_field.setter
    def map_field(self, value: dict[Enum3, Enum4]):
      self._native.map_field = _unwrap(value, dict[Enum3, Enum4])


