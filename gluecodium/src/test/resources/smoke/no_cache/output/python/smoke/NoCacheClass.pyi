

import typing

from _native_base import _NativeBase

import generated


class NoCacheClass(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make() -> NoCacheClass: ...

    def foo(self): ...

