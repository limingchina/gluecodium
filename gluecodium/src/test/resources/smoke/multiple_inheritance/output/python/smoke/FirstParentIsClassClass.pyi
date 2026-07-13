

from smoke.ParentClass import ParentClass
from smoke.ParentNarrowOne import ParentNarrowOne

from _native_base import _NativeBase


class FirstParentIsClassClass(
    ParentClass,
    ParentNarrowOne)(_NativeBase):
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


