

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class OuterClassInnerClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def foo(self, input: str) -> str:
        """"""
        return _wrap(self._native.foo(_unwrap(input, str)), str)

