

from smoke.SingleNamedConstructor import SingleNamedConstructor

from _native_base import _NativeBase


class SingleNamedConstructor(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def create(self) -> SingleNamedConstructor:
        """"""
        return self._native.create()

