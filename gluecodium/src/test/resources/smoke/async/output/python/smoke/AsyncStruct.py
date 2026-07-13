

from __future__ import annotations

from smoke.ThrowMeError import ThrowMeError


from _native_base import _NativeBase

import generated


class AsyncStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], AsyncStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.AsyncStruct(*args))


    @property
    def string_field(self) -> str:
        """"""
        return self._native.string_field

    @string_field.setter
    def string_field(self, value: str):
        self._native.string_field = value



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
        native_result = generated.AsyncStruct.async_static(input)
        return None(native_result)

