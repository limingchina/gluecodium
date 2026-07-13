

from smoke.InterfaceWithOverloads import InterfaceWithOverloads

from _native_base import _NativeBase


class ChildClassNameClash(
    InterfaceWithOverloads)(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

