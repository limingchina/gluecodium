

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

import datetime

class DurationOverloads(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    def duration_function(self, *args, **kwargs) -> str:
        return _wrap(self._native.duration_function(*[_unwrap(a) for a in args]), str)



