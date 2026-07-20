

import typing

from _native_base import _NativeBase

import generated


class JavaMethodOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def one(self, input: str): ...

    def two(self, input: list[str]): ...

