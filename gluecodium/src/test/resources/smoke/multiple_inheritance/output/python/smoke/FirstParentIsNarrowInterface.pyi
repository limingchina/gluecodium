

from smoke.ParentNarrowOne import ParentNarrowOne
from smoke.ParentNarrowTwo import ParentNarrowTwo


from _native_base import _NativeBase

import generated


class FirstParentIsNarrowInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, FirstParentIsNarrowInterface):
            super().__init__(native)
        else:
            super().__init__(generated.FirstParentIsNarrowInterface())


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

