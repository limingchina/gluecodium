

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.AsyncError import AsyncError
from smoke.AsyncErrorCode import AsyncErrorCode

from _native_base import _NativeBase

import generated


class AsyncClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def async_void(self, input: bool):
        """"""
        return _wrap(self._native.async_void(_unwrap(input, bool)), None)

    def async_void_throws(self, input: bool):
        """"""
        return _wrap(self._native.async_void_throws(_unwrap(input, bool)), None)

    def async_int(self, input: bool) -> int:
        """"""
        return _wrap(self._native.async_int(_unwrap(input, bool)), int)

    def async_int_throws(self, input: bool) -> int:
        """"""
        return _wrap(self._native.async_int_throws(_unwrap(input, bool)), int)

    @staticmethod
    def async_static(input: bool):
        """"""
        generated.AsyncClass.async_static(_unwrap(input, bool))

