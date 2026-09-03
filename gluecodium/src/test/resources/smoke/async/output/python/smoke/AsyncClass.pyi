

from smoke.AsyncError import AsyncError
from smoke.AsyncErrorCode import AsyncErrorCode
from enum import Enum
import typing

class AsyncClass:

    def async_void(self, input: bool):
        ...

    def async_void_throws(self, input: bool):
        ...

    def async_int(self, input: bool) -> int:
        ...

    def async_int_throws(self, input: bool) -> int:
        ...

    @staticmethod
    def async_static(input: bool):
        ...


