

from smoke.ChildWithCustomConstructor import ChildWithCustomConstructor
from smoke.ParentWithCustomConstructor import ParentWithCustomConstructor

from _native_base import _NativeBase


class ChildWithCustomConstructor(
    ParentWithCustomConstructor)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def make(self) -> ChildWithCustomConstructor:
        """"""
        return self._native.make()

