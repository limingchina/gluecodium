

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class ExternalClasssome_Struct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_ExternalClasssome_Struct):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_ExternalClasssome_Struct(*[_unwrap(arg) for arg in args]))


    @property
    def some_field(self) -> str:
        """"""
        return _wrap(self._native.some_field, str)
    @some_field.setter
    def some_field(self, value: str):
      self._native.some_field = _unwrap(value, str)


