

from __future__ import annotations



from _native_base import _NativeBase

import generated


class SomeSkippedStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SomeSkippedStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.SomeSkippedStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def field(self) -> list[SomeSkippedEnum]:
        """"""
        return self._native.field
    @field.setter
    def field(self, value: list[SomeSkippedEnum]):
      self._native.field = getattr(value, "_native", value)


