

from smoke.ParentNarrowOne import ParentNarrowOne
from smoke.ParentNarrowTwo import ParentNarrowTwo

class FirstParentIsNarrowInterface:
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


