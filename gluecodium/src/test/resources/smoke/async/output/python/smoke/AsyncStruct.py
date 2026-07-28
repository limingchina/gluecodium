

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.ThrowMeError import ThrowMeError


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
        generated.smoke_AsyncStruct.async_static(_unwrap(input, bool))

