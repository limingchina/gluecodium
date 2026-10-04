

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated


class SkipPlatforms(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def not_in_java(input: str) -> str:
        return _wrap(generated.smoke_SkipPlatforms.not_in_java(_unwrap(input, str)), str)

    @staticmethod
    def not_in_swift(input: bool) -> bool:
        return _wrap(generated.smoke_SkipPlatforms.not_in_swift(_unwrap(input, bool)), bool)

    @staticmethod
    def not_in_dart(input: float) -> float:
        return _wrap(generated.smoke_SkipPlatforms.not_in_dart(_unwrap(input, float)), float)

    @staticmethod
    def not_in_kotlin(input: float) -> float:
        return _wrap(generated.smoke_SkipPlatforms.not_in_kotlin(_unwrap(input, float)), float)


