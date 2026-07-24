

from smoke.StructA import StructA
import typing


from _native_base import _NativeBase

import generated


class StructB(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructB):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructB(*[_unwrap(arg) for arg in args]))


    @property
    def field(self) -> list[StructA]:
        """"""
        return _wrap(self._native.field, list[StructA])
    @field.setter
    def field(self, value: list[StructA]):
      self._native.field = _unwrap(value, list[StructA])


