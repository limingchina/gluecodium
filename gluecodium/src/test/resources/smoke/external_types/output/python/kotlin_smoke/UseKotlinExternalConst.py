

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from kotlin_smoke.VeryBoolean import VeryBoolean


from _native_base import _NativeBase

import generated


class UseKotlinExternalConst(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.kotlin_smoke_UseKotlinExternalConst):
            super().__init__(args[0])
        else:
            super().__init__(generated.kotlin_smoke_UseKotlinExternalConst(
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



    DEFAULT_TRUTH = {true}

