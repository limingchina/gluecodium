

from __future__ import annotations

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
        return self._native.async_void(input)

    def async_void_throws(self, input: bool):
        """"""
        return self._native.async_void_throws(input)

    def async_int(self, input: bool) -> int:
        """"""
        return self._native.async_int(input)

    def async_int_throws(self, input: bool) -> int:
        """"""
        return self._native.async_int_throws(input)

    @staticmethod
    def async_static(input: bool):
        """"""
        generated.AsyncClass.async_static(input)

