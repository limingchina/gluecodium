

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class NoCacheClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make() -> NoCacheClass:
        """"""
        native_result = generated.smoke_NoCacheClass.make()
        return NoCacheClass(native_result)

    def foo(self):
        """"""
        return _wrap(self._native.foo(), None)

