

from smoke.StructB import StructB
import typing


from _native_base import _NativeBase

import generated


class StructA(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructA):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructA(*[_unwrap(arg) for arg in args]))


    @property
    def field(self) -> list[StructB]:
        """"""
        return _wrap(self._native.field, list[StructB])
    @field.setter
    def field(self, value: list[StructB]):
      self._native.field = _unwrap(value, list[StructB])


