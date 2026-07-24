

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class UnusedTopLevelPoint(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.UnusedTopLevelPoint):
            super().__init__(args[0])
        else:
            super().__init__(generated.UnusedTopLevelPoint(*[_unwrap(arg) for arg in args]))


    @property
    def foo(self) -> str:
        """"""
        return _wrap(self._native.foo, str)
    @foo.setter
    def foo(self, value: str):
      self._native.foo = _unwrap(value, str)


