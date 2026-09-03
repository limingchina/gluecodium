

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class DartPublicElementsEnabled(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DartPublicElementsEnabled):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DartPublicElementsEnabled(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def bool_field(self) -> bool:
        return _wrap(self._native.bool_field, bool)
    @bool_field.setter
    def bool_field(self, value: bool):
      self._native.bool_field = _unwrap(value, bool)


    @property
    def _string_field(self) -> str:
        return _wrap(self._native._string_field, str)
    @_string_field.setter
    def _string_field(self, value: str):
      self._native._string_field = _unwrap(value, str)


    def _foo(self):
        return _wrap(self._native._foo(), None)


