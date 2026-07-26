

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from _native_base import _NativeBase

import generated


class SwiftConstructorOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make(input: str) -> SwiftConstructorOverloads:
        """"""
        native_result = generated.smoke_SwiftConstructorOverloads.make(_unwrap(input, str))
        return SwiftConstructorOverloads(native_result)

    @staticmethod
    def make_do(throughput: str) -> SwiftConstructorOverloads:
        """"""
        native_result = generated.smoke_SwiftConstructorOverloads.make_do(_unwrap(throughput, str))
        return SwiftConstructorOverloads(native_result)

