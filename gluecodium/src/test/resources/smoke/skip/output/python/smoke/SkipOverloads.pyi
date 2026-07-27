

import typing


from _native_base import _NativeBase

import generated


class SkipOverloads(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_SkipOverloads):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_SkipOverloads(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def dummy(self) -> float:
        """"""
        return _wrap(self._native.dummy, float)
    @dummy.setter
    def dummy(self, value: float):
      self._native.dummy = _unwrap(value, float)


    def do_foo(self, input: float): ...

