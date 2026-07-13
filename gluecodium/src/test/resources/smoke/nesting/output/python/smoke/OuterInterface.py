

from __future__ import annotations



from _native_base import _NativeBase

import generated


class OuterInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, OuterInterface):
            super().__init__(native)
        else:
            super().__init__(generated.OuterInterface())


    def foo(self, input: str) -> str:
        """"""
        return self._native.foo(input)

