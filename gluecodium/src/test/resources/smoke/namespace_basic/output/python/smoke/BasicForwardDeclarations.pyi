

from smoke.Basic import Basic

from _native_base import _NativeBase


class BasicForwardDeclarations(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def use_basic(self) -> Basic:
        """"""
        return self._native.use_basic()

