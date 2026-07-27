

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional



from _native_base import _NativeBase

import generated


class PublicStructWithInternalConstructors(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_PublicStructWithInternalConstructors):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_PublicStructWithInternalConstructors(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


    @property
    def some_var(self) -> int:
        """"""
        return _wrap(self._native.some_var, int)
    @some_var.setter
    def some_var(self, value: int):
      self._native.some_var = _unwrap(value, int)


    @staticmethod
    def make() -> PublicStructWithInternalConstructors:
        """"""
        native_result = generated.smoke_PublicStructWithInternalConstructors.make()
        return PublicStructWithInternalConstructors(native_result)

