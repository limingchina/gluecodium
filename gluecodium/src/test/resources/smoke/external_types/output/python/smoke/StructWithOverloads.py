

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional



from _native_base import _NativeBase

import generated


class StructWithOverloads(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructWithOverloads):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructWithOverloads(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def overloaded_accessors(self) -> int:
        """"""
        return _wrap(self._native.overloaded_accessors, int)
    @overloaded_accessors.setter
    def overloaded_accessors(self, value: int):
      self._native.overloaded_accessors = _unwrap(value, int)


    def overloaded_method(*args, **kwargs) -> str:
        """"""
        return _wrap(self._native.overloaded_method(*[_unwrap(a) for a in args]), str)



