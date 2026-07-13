

from smoke.JavaExternalCtor import JavaExternalCtor

from _native_base import _NativeBase


class JavaExternalCtor(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    field: str


    def make(self, field: str) -> JavaExternalCtor:
        """"""
        return self._native.make(field)

