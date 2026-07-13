

from __future__ import annotations

from another.SomeCoolClassType import SomeCoolClassType
from smoke.ParentInterface import ParentInterface
from smoke.ParentNarrowOne import ParentNarrowOne


from _native_base import _NativeBase

import generated


class FirstParentIsInterfaceInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, FirstParentIsInterfaceInterface):
            super().__init__(native)
        else:
            super().__init__(generated.FirstParentIsInterfaceInterface())


    def child_function(self):
        """"""
        return self._native.child_function()


    @property
    def child_property(self) -> str:
        """"""
        return self._native.child_property

    @child_property.setter
    def child_property(self, value: str):
        self._native.child_property = value

