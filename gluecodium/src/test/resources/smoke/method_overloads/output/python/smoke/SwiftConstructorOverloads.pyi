

from smoke.SwiftConstructorOverloads import SwiftConstructorOverloads

from _native_base import _NativeBase


class SwiftConstructorOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def make(self, input: str) -> SwiftConstructorOverloads:
        """"""
        return self._native.make(input)


    def make_do(self, throughput: str) -> SwiftConstructorOverloads:
        """"""
        return self._native.make_do(throughput)

