

from smoke.ThrowMeError import ThrowMeError
import typing

class AsyncStruct:

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

