

import typing

from _native_base import _NativeBase

import generated


class SwiftConstructorOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make(input: str) -> SwiftConstructorOverloads: ...

    @staticmethod
    def make_do(throughput: str) -> SwiftConstructorOverloads: ...

