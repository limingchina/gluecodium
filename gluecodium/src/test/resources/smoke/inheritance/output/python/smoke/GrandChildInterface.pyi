

from smoke.ChildInterface import ChildInterface

from _native_base import _NativeBase


class GrandChildInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def grand_child_method(self):
        """"""
        return self._native.grand_child_method()

