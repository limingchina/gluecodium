

from __future__ import annotations



from _native_base import _NativeBase

import generated


class StructWithList(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructWithList):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithList(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def field(self) -> list[StructWithList]:
        """"""
        return self._native.field

    @field.setter
    def field(self, value: list[StructWithList]):
      self._native.field = getattr(value, "_native", value)


