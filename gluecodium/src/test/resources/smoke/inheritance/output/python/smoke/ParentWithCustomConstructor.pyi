

from smoke.ParentWithCustomConstructor import ParentWithCustomConstructor

from _native_base import _NativeBase


class ParentWithCustomConstructor(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def create(self) -> ParentWithCustomConstructor:
        """"""
        return self._native.create()

