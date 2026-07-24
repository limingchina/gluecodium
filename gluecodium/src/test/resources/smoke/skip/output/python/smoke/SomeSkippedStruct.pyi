

from smoke.SomeSkippedEnum import SomeSkippedEnum
import typing


from _native_base import _NativeBase

import generated


class SomeSkippedStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SomeSkippedStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.SomeSkippedStruct(*[_unwrap(arg) for arg in args]))


    @property
    def field(self) -> list[SomeSkippedEnum]:
        """"""
        return _wrap(self._native.field, list[SomeSkippedEnum])
    @field.setter
    def field(self, value: list[SomeSkippedEnum]):
      self._native.field = _unwrap(value, list[SomeSkippedEnum])


