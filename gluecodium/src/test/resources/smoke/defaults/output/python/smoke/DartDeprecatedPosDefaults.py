

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class DartDeprecatedPosDefaults(_NativeBase):
    """Foo Bar this is a comment"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DartDeprecatedPosDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.DartDeprecatedPosDefaults(*[_unwrap(arg) for arg in args]))


    @property
    def int_field(self) -> int:
        """"""
        return _wrap(self._native.int_field, int)
    @int_field.setter
    def int_field(self, value: int):
      self._native.int_field = _unwrap(value, int)



    @property
    def string_field(self) -> str:
        """"""
        return _wrap(self._native.string_field, str)
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = _unwrap(value, str)


