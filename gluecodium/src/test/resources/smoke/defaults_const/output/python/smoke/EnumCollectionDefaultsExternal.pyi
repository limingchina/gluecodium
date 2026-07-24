

from fire.ExternalEnum1 import ExternalEnum1
from fire.ExternalEnum2 import ExternalEnum2
from fire.ExternalEnum3 import ExternalEnum3
from fire.ExternalEnum4 import ExternalEnum4
import typing


from _native_base import _NativeBase

import generated


class EnumCollectionDefaultsExternal(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumCollectionDefaultsExternal):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumCollectionDefaultsExternal(*[_unwrap(arg) for arg in args]))


    @property
    def list_field(self) -> list[ExternalEnum1]:
        """"""
        return _wrap(self._native.list_field, list[ExternalEnum1])
    @list_field.setter
    def list_field(self, value: list[ExternalEnum1]):
      self._native.list_field = _unwrap(value, list[ExternalEnum1])



    @property
    def set_field(self) -> set[ExternalEnum2]:
        """"""
        return _wrap(self._native.set_field, set[ExternalEnum2])
    @set_field.setter
    def set_field(self, value: set[ExternalEnum2]):
      self._native.set_field = _unwrap(value, set[ExternalEnum2])



    @property
    def map_field(self) -> dict[ExternalEnum3, ExternalEnum4]:
        """"""
        return _wrap(self._native.map_field, dict[ExternalEnum3, ExternalEnum4])
    @map_field.setter
    def map_field(self, value: dict[ExternalEnum3, ExternalEnum4]):
      self._native.map_field = _unwrap(value, dict[ExternalEnum3, ExternalEnum4])


