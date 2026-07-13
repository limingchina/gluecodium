

from __future__ import annotations



from _native_base import _NativeBase

import generated


class SkipPlatforms(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def not_in_java(input: str) -> str:
        """"""
        native_result = generated.SkipPlatforms.not_in_java(input)
        return str(native_result)

    @staticmethod

    def not_in_swift(input: bool) -> bool:
        """"""
        native_result = generated.SkipPlatforms.not_in_swift(input)
        return bool(native_result)

    @staticmethod

    def not_in_dart(input: float) -> float:
        """"""
        native_result = generated.SkipPlatforms.not_in_dart(input)
        return float(native_result)

    @staticmethod

    def not_in_kotlin(input: float) -> float:
        """"""
        native_result = generated.SkipPlatforms.not_in_kotlin(input)
        return float(native_result)

