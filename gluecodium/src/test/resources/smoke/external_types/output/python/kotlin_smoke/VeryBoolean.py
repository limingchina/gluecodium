

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class VeryBoolean(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.VeryBoolean):
            super().__init__(args[0])
        else:
            super().__init__(generated.VeryBoolean(*[_unwrap(arg) for arg in args]))


    @property
    def value(self) -> bool:
        """"""
        return _wrap(self._native.value, bool)
    @value.setter
    def value(self, value: bool):
      self._native.value = _unwrap(value, bool)


    @staticmethod
    def make(value: bool) -> VeryBoolean:
        """"""
        native_result = generated.VeryBoolean.make(_unwrap(value, bool))
        return VeryBoolean(native_result)

