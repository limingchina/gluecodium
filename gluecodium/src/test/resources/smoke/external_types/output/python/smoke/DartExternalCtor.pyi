

from smoke.DartExternalCtor import DartExternalCtor

from _native_base import _NativeBase


class DartExternalCtor(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    field: str


    def make(self, field: str) -> DartExternalCtor:
        """"""
        return self._native.make(field)

