

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class SkipFunctions(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def not_in_java(input: str) -> str:
        return generated.smoke_SkipFunctions.not_in_java(_unwrap(input, str))

    @staticmethod
    def not_in_swift(input: bool) -> bool:
        return generated.smoke_SkipFunctions.not_in_swift(_unwrap(input, bool))

    @staticmethod
    def not_in_dart(input: float) -> float:
        return generated.smoke_SkipFunctions.not_in_dart(_unwrap(input, float))

    @staticmethod
    def not_in_kotlin(input: str) -> str:
        return generated.smoke_SkipFunctions.not_in_kotlin(_unwrap(input, str))


