

from smoke.ThrowMeError import ThrowMeError

from _native_base import _NativeBase


class AsyncStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    string_field: str


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


    def async_static(self, input: bool):
        """"""
        return self._native.async_static(input)

