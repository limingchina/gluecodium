

from smoke.AsyncErrorCode import AsyncErrorCode
import typing

from _native_base import _NativeBase

import generated


class AsyncClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def async_void(self, input: bool): ...

    def async_void_throws(self, input: bool): ...

    def async_int(self, input: bool) -> int: ...

    def async_int_throws(self, input: bool) -> int: ...

    @staticmethod
    def async_static(input: bool): ...

