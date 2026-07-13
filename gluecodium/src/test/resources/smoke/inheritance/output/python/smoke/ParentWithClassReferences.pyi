

from smoke.ChildClassFromClass import ChildClassFromClass
from smoke.ParentClass import ParentClass

from _native_base import _NativeBase


class ParentWithClassReferences(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def class_function(self) -> ChildClassFromClass:
        """"""
        return self._native.class_function()


    @property
    def class_property(self) -> ParentClass:
        """"""
        return self._native.class_property


