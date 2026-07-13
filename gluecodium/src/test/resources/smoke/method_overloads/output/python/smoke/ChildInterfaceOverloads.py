

from __future__ import annotations

from smoke.ParentInterface import ParentInterface


from _native_base import _NativeBase

import generated


class ChildInterfaceOverloads(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ChildInterfaceOverloads):
            super().__init__(native)
        else:
            super().__init__(generated.ChildInterfaceOverloads())


    def foo(self, input: str):
        """"""
        return self._native.foo(input)


    def bar(self, input: str):
        """"""
        return self._native.bar(input)

