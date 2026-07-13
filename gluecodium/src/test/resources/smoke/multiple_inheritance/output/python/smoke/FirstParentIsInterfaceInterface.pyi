

from another.SomeCoolClassType import SomeCoolClassType
from smoke.ParentInterface import ParentInterface
from smoke.ParentNarrowOne import ParentNarrowOne

from _native_base import _NativeBase


class FirstParentIsInterfaceInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def child_function(self):
        """"""
        return self._native.child_function()


    @property
    def child_property(self) -> str:
        """"""
        return self._native.child_property


