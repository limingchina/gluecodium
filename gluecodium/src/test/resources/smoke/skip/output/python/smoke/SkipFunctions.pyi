

import typing

from _native_base import _NativeBase

import generated


class SkipFunctions(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def not_in_java(input: str) -> str: ...

    @staticmethod
    def not_in_swift(input: bool) -> bool: ...

    @staticmethod
    def not_in_dart(input: float) -> float: ...

    @staticmethod
    def not_in_kotlin(input: str) -> str: ...

