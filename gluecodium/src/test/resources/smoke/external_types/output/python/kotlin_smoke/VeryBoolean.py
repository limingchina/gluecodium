

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class VeryBoolean(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.kotlin_smoke_VeryBoolean):
            super().__init__(args[0])
        else:
            super().__init__(generated.kotlin_smoke_VeryBoolean(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def value(self) -> bool:
        return _wrap(self._native.value, bool)
    @value.setter
    def value(self, value: bool):
      self._native.value = _unwrap(value, bool)


    @staticmethod
    def make(value: bool) -> VeryBoolean:
        native_result = generated.kotlin_smoke_VeryBoolean.make(_unwrap(value, bool))
        return _get_or_create_wrapper(native_result, VeryBoolean)


