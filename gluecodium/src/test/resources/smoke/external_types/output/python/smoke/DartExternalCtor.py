

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class DartExternalCtor(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DartExternalCtor):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DartExternalCtor(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def field(self) -> str:
        """"""
        return _wrap(self._native.field, str)
    @field.setter
    def field(self, value: str):
      self._native.field = _unwrap(value, str)


    @staticmethod
    def make(field: str) -> DartExternalCtor:
        """"""
        native_result = generated.smoke_DartExternalCtor.make(_unwrap(field, str))
        return DartExternalCtor(native_result)

