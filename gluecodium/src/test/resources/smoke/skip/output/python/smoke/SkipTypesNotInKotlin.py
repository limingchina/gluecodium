

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional



from _native_base import _NativeBase

import generated


class SkipTypesNotInKotlin(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_SkipTypesNotInKotlin):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_SkipTypesNotInKotlin(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def foo_field(self) -> str:
        return _wrap(self._native.foo_field, str)
    @foo_field.setter
    def foo_field(self, value: str):
      self._native.foo_field = _unwrap(value, str)


