

from __future__ import annotations



from _native_base import _NativeBase

import generated


class ParentInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ParentInterface):
            super().__init__(native)
        else:
            super().__init__(generated.ParentInterface())


    def foo(self):
        """"""
        return self._native.foo()


    def foo(self, input: int):
        """"""
        return self._native.foo(input)


    def bar(self):
        """"""
        return self._native.bar()


    def baz(self):
        """"""
        return self._native.baz()

