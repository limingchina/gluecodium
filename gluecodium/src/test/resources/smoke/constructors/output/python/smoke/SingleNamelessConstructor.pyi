

from smoke.SingleNamelessConstructor import SingleNamelessConstructor

from _native_base import _NativeBase


class SingleNamelessConstructor(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def create(self) -> SingleNamelessConstructor:
        """"""
        return self._native.create()

