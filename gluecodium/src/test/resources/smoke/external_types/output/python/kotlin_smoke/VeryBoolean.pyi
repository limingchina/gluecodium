

from kotlin_smoke.VeryBoolean import VeryBoolean

from _native_base import _NativeBase


class VeryBoolean(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    value: bool


    def make(self, value: bool) -> VeryBoolean:
        """"""
        return self._native.make(value)

