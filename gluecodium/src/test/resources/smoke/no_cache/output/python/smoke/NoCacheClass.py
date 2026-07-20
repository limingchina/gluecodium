

from __future__ import annotations


from _native_base import _NativeBase

import generated


class NoCacheClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make() -> NoCacheClass:
        """"""
        native_result = generated.NoCacheClass.make()
        return NoCacheClass(native_result)

    def foo(self):
        """"""
        return self._native.foo()

