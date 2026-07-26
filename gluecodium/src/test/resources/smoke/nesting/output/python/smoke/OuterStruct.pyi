

import datetime
from smoke.OuterStructInnerEnum import OuterStructInnerEnum
from smoke.OuterStructInstantiation import OuterStructInstantiation
import typing


from _native_base import _NativeBase

import generated


class OuterStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_OuterStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_OuterStruct(*[_unwrap(arg) for arg in args]))


    @property
    def field(self) -> str:
        """"""
        return _wrap(self._native.field, str)
    @field.setter
    def field(self, value: str):
      self._native.field = _unwrap(value, str)


    def do_nothing(self): ...

