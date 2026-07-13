

from __future__ import annotations

from another.SomeCoolClassType import SomeCoolClassType


from _native_base import _NativeBase

import generated


class ParentInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ParentInterface):
            super().__init__(native)
        else:
            super().__init__(generated.ParentInterface())


    def parent_function(self):
        """"""
        return self._native.parent_function()


    def some_function_that_uses_type_from_another_package(self, some_param: SomeCoolClassType):
        """"""
        return self._native.some_function_that_uses_type_from_another_package(some_param._native)


    @property
    def parent_property(self) -> str:
        """"""
        return self._native.parent_property

    @parent_property.setter
    def parent_property(self, value: str):
        self._native.parent_property = value

