

from smoke.ThrowMeError import ThrowMeError
from enum import Enum
import typing
from typing import Optional

class AsyncStruct:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, string_field: str) -> None: ...

    string_field: str

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
