

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class NullableOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def foo(*args, **kwargs):
        """"""
        return _wrap(self._native.foo(*[_unwrap(a) for a in args]), None)


