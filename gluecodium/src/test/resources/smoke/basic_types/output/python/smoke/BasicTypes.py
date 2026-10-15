

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base, _struct_key
from enum import Enum
from typing import Optional
import generated


class BasicTypes(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def string_function(input: str) -> str:
        return _wrap(generated.smoke_BasicTypes.string_function(_unwrap(input, str)), str)

    @staticmethod
    def bool_function(input: bool) -> bool:
        return _wrap(generated.smoke_BasicTypes.bool_function(_unwrap(input, bool)), bool)

    @staticmethod
    def float_function(input: float) -> float:
        return _wrap(generated.smoke_BasicTypes.float_function(_unwrap(input, float)), float)

    @staticmethod
    def double_function(input: float) -> float:
        return _wrap(generated.smoke_BasicTypes.double_function(_unwrap(input, float)), float)

    @staticmethod
    def byte_function(input: int) -> int:
        return _wrap(generated.smoke_BasicTypes.byte_function(_unwrap(input, int)), int)

    @staticmethod
    def short_function(input: int) -> int:
        return _wrap(generated.smoke_BasicTypes.short_function(_unwrap(input, int)), int)

    @staticmethod
    def int_function(input: int) -> int:
        return _wrap(generated.smoke_BasicTypes.int_function(_unwrap(input, int)), int)

    @staticmethod
    def long_function(input: int) -> int:
        return _wrap(generated.smoke_BasicTypes.long_function(_unwrap(input, int)), int)

    @staticmethod
    def ubyte_function(input: int) -> int:
        return _wrap(generated.smoke_BasicTypes.ubyte_function(_unwrap(input, int)), int)

    @staticmethod
    def ushort_function(input: int) -> int:
        return _wrap(generated.smoke_BasicTypes.ushort_function(_unwrap(input, int)), int)

    @staticmethod
    def uint_function(input: int) -> int:
        return _wrap(generated.smoke_BasicTypes.uint_function(_unwrap(input, int)), int)

    @staticmethod
    def ulong_function(input: int) -> int:
        return _wrap(generated.smoke_BasicTypes.ulong_function(_unwrap(input, int)), int)
