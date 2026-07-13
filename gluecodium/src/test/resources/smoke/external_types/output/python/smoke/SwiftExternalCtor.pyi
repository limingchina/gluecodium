

from smoke.SwiftExternalCtor import SwiftExternalCtor

from _native_base import _NativeBase


class SwiftExternalCtor(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    field: str


    def make(self, field: str) -> SwiftExternalCtor:
        """"""
        return self._native.make(field)

