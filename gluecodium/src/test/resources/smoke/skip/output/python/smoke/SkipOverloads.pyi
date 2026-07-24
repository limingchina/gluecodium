

import typing


from _native_base import _NativeBase

import generated


class SkipOverloads(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.SkipOverloads):
            super().__init__(args[0])
        else:
            super().__init__(generated.SkipOverloads(*[_unwrap(arg) for arg in args]))


    @property
    def dummy(self) -> float:
        """"""
        return _wrap(self._native.dummy, float)
    @dummy.setter
    def dummy(self, value: float):
      self._native.dummy = _unwrap(value, float)


    def do_foo(self, input: float): ...

