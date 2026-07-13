

from __future__ import annotations

from smoke.ChildClassFromClass import ChildClassFromClass
from smoke.ParentClass import ParentClass


from _native_base import _NativeBase

import generated


class ParentWithClassReferences(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ParentWithClassReferences):
            super().__init__(native)
        else:
            super().__init__(generated.ParentWithClassReferences())


    def class_function(self) -> ChildClassFromClass:
        """"""
        return self._native.class_function()


    @property
    def class_property(self) -> ParentClass:
        """"""
        return self._native.class_property

    @class_property.setter
    def class_property(self, value: ParentClass):
        self._native.class_property = value

