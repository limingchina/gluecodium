

from __future__ import annotations

import datetime

from _native_base import _NativeBase

import generated


class DurationOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def duration_function(*args, **kwargs) -> str:
        """"""
        return self._native.duration_function(*[getattr(a, "_native", a) for a in args])


