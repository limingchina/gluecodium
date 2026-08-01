

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class NoCacheClass(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make() -> NoCacheClass:
        native_result = generated.smoke_NoCacheClass.make()
        return _get_or_create_wrapper(native_result, NoCacheClass)

    def foo(self):
        return _wrap(self._native.foo(), None)


