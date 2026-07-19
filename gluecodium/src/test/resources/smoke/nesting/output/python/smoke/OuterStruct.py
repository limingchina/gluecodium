

from __future__ import annotations

from smoke.OuterStructInnerEnum import OuterStructInnerEnum


from _native_base import _NativeBase

import generated


class OuterStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OuterStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.OuterStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def field(self) -> str:
        """"""
        return self._native.field
    @field.setter
    def field(self, value: str):
      self._native.field = getattr(value, "_native", value)


    def do_nothing(self):
        """"""
        return self._native.do_nothing()

