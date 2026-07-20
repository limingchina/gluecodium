

from __future__ import annotations


from _native_base import _NativeBase

import generated


class SwiftConstructorOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make(input: str) -> SwiftConstructorOverloads:
        """"""
        native_result = generated.SwiftConstructorOverloads.make(input)
        return SwiftConstructorOverloads(native_result)

    @staticmethod
    def make_do(throughput: str) -> SwiftConstructorOverloads:
        """"""
        native_result = generated.SwiftConstructorOverloads.make_do(throughput)
        return SwiftConstructorOverloads(native_result)

