

import typing


from _native_base import _NativeBase

import generated


class JavaExternalCtor(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_JavaExternalCtor):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_JavaExternalCtor(*[_unwrap(arg) for arg in args]))


    @property
    def field(self) -> str:
        """"""
        return _wrap(self._native.field, str)
    @field.setter
    def field(self, value: str):
      self._native.field = _unwrap(value, str)


    @staticmethod
    def make(field: str) -> JavaExternalCtor: ...

