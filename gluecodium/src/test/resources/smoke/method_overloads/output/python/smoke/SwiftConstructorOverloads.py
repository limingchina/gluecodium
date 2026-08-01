

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class SwiftConstructorOverloads(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def make(input: str) -> SwiftConstructorOverloads:
        native_result = generated.smoke_SwiftConstructorOverloads.make(_unwrap(input, str))
        return _get_or_create_wrapper(native_result, SwiftConstructorOverloads)

    @staticmethod
    def make_do(throughput: str) -> SwiftConstructorOverloads:
        native_result = generated.smoke_SwiftConstructorOverloads.make_do(_unwrap(throughput, str))
        return _get_or_create_wrapper(native_result, SwiftConstructorOverloads)


