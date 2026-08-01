

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class AsyncWithSkips(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make_shared_instance(*args, **kwargs):
        generated.smoke_AsyncWithSkips.make_shared_instance(*[_unwrap(a) for a in args])



