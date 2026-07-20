

from __future__ import annotations


from _native_base import _NativeBase

import generated


class NullableOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def foo(*args, **kwargs):
        """"""
        return self._native.foo(*[getattr(a, "_native", a) for a in args])


