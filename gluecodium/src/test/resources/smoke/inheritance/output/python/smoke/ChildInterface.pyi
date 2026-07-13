

from smoke.ParentInterface import ParentInterface

from _native_base import _NativeBase


class ChildInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def child_method(self):
        """"""
        return self._native.child_method()

