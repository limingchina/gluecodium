

from another.SomeCoolClassType import SomeCoolClassType
from smoke.ParentInterface import ParentInterface
from smoke.ParentNarrowOne import ParentNarrowOne

class FirstParentIsInterfaceInterface:
    """"""

    def __init__(self, native):
        self._native = native


    def child_function(self):
        """"""
        return self._native.child_function()


    @property
    def child_property(self) -> str:
        """"""
        return self._native.child_property


