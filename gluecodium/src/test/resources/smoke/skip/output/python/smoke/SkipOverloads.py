

from __future__ import annotations



from _native_base import _NativeBase

import generated


class SkipOverloads(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], SkipOverloads):
            super().__init__(args[0])
        else:
            super().__init__(generated.SkipOverloads(*args))


    @property
    def dummy(self) -> float:
        """"""
        return self._native.dummy

    @dummy.setter
    def dummy(self, value: float):
        self._native.dummy = value



    def do_foo(self, input: float):
        """"""
        return self._native.do_foo(input)

