

from __future__ import annotations

from smoke.MethodOverloadsPoint import MethodOverloadsPoint

from _native_base import _NativeBase

import generated


class MethodOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def is_boolean(*args, **kwargs) -> bool:
        """"""
        return self._native.is_boolean(*[getattr(a, "_native", a) for a in args])








    def is_float(*args, **kwargs) -> bool:
        """"""
        return self._native.is_float(*[getattr(a, "_native", a) for a in args])


