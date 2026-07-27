

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.StructA import StructA


from _native_base import _NativeBase

import generated


class StructB(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructB):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructB(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def field(self) -> list[StructA]:
        """"""
        return _wrap(self._native.field, list[StructA])
    @field.setter
    def field(self, value: list[StructA]):
      self._native.field = _unwrap(value, list[StructA])


