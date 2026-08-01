

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class Payload(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Payload):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_Payload(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def error_code(self) -> int:
        return _wrap(self._native.error_code, int)
    @error_code.setter
    def error_code(self, value: int):
      self._native.error_code = _unwrap(value, int)


    @property
    def message(self) -> str:
        return _wrap(self._native.message, str)
    @message.setter
    def message(self, value: str):
      self._native.message = _unwrap(value, str)



