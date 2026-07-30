

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from _native_base import _NativeBase

import generated


class BasicTypes(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def string_function(input: str) -> str:
        return generated.smoke_BasicTypes.string_function(_unwrap(input, str))

    @staticmethod
    def bool_function(input: bool) -> bool:
        return generated.smoke_BasicTypes.bool_function(_unwrap(input, bool))

    @staticmethod
    def float_function(input: float) -> float:
        return generated.smoke_BasicTypes.float_function(_unwrap(input, float))

    @staticmethod
    def double_function(input: float) -> float:
        return generated.smoke_BasicTypes.double_function(_unwrap(input, float))

    @staticmethod
    def byte_function(input: int) -> int:
        return generated.smoke_BasicTypes.byte_function(_unwrap(input, int))

    @staticmethod
    def short_function(input: int) -> int:
        return generated.smoke_BasicTypes.short_function(_unwrap(input, int))

    @staticmethod
    def int_function(input: int) -> int:
        return generated.smoke_BasicTypes.int_function(_unwrap(input, int))

    @staticmethod
    def long_function(input: int) -> int:
        return generated.smoke_BasicTypes.long_function(_unwrap(input, int))

    @staticmethod
    def ubyte_function(input: int) -> int:
        return generated.smoke_BasicTypes.ubyte_function(_unwrap(input, int))

    @staticmethod
    def ushort_function(input: int) -> int:
        return generated.smoke_BasicTypes.ushort_function(_unwrap(input, int))

    @staticmethod
    def uint_function(input: int) -> int:
        return generated.smoke_BasicTypes.uint_function(_unwrap(input, int))

    @staticmethod
    def ulong_function(input: int) -> int:
        return generated.smoke_BasicTypes.ulong_function(_unwrap(input, int))

