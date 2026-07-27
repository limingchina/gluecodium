

from smoke.ThrowMeError import ThrowMeError
import typing


from _native_base import _NativeBase

import generated


class AsyncStruct(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_AsyncStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_AsyncStruct(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def string_field(self) -> str:
        """"""
        return _wrap(self._native.string_field, str)
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = _unwrap(value, str)


    def async_void(self, input: bool): ...

    def async_void_throws(self, input: bool): ...

    def async_int(self, input: bool) -> int: ...

    def async_int_throws(self, input: bool) -> int: ...

    @staticmethod
    def async_static(input: bool): ...

