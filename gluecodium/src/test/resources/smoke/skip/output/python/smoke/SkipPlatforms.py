

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
        return generated.SkipPlatforms.not_in_java(input)

    @staticmethod
    def not_in_swift(input: bool) -> bool:
        """"""
        return generated.SkipPlatforms.not_in_swift(input)

    @staticmethod
    def not_in_dart(input: float) -> float:
        """"""
        return generated.SkipPlatforms.not_in_dart(input)

    @staticmethod
    def not_in_kotlin(input: float) -> float:
        """"""
        return generated.SkipPlatforms.not_in_kotlin(input)

