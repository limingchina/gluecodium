

import typing


from _native_base import _NativeBase

import generated


class FieldConstructorsSkipTag(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_FieldConstructorsSkipTag):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_FieldConstructorsSkipTag(*[_unwrap(arg) for arg in args]))


    @property
    def field1(self) -> str:
        """"""
        return _wrap(self._native.field1, str)
    @field1.setter
    def field1(self, value: str):
      self._native.field1 = _unwrap(value, str)


