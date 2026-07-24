

import typing


from _native_base import _NativeBase

import generated


class TypeDefsTestStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.TypeDefsTestStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypeDefsTestStruct(*[_unwrap(arg) for arg in args]))


    @property
    def something(self) -> str:
        """"""
        return _wrap(self._native.something, str)
    @something.setter
    def something(self, value: str):
      self._native.something = _unwrap(value, str)


