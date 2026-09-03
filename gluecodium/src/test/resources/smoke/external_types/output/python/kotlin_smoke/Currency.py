

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class Currency(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.kotlin_smoke_Currency):
            super().__init__(args[0])
        else:
            super().__init__(generated.kotlin_smoke_Currency(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def currency_code(self) -> str:
        return _wrap(self._native.currency_code, str)


    @property
    def numeric_code(self) -> int:
        return _wrap(self._native.numeric_code, int)



