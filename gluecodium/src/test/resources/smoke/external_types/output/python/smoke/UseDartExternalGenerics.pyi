

import typing

from _native_base import _NativeBase

import generated


class UseDartExternalGenerics(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def use_generics(self, list: list[Rectangle], set: set[CompressionState]) -> dict[CompressionState, Rectangle]: ...

