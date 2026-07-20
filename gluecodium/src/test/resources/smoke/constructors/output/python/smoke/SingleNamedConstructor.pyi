

import typing

from _native_base import _NativeBase

import generated


class SingleNamedConstructor(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def create() -> SingleNamedConstructor: ...

