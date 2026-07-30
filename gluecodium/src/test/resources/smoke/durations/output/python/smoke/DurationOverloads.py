

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

import datetime

from _native_base import _NativeBase

import generated


class DurationOverloads(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def duration_function(*args, **kwargs) -> str:
        return _wrap(self._native.duration_function(*[_unwrap(a) for a in args]), str)


