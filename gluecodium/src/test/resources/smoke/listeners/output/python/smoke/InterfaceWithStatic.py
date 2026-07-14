

from __future__ import annotations



from _native_base import _NativeBase

import generated


class InterfaceWithStatic(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, InterfaceWithStatic):
            super().__init__(native)
        else:
            super().__init__(generated.InterfaceWithStatic())

    def regular_function(self) -> str:
        """"""
        return self._native.regular_function()

    @staticmethod
    def static_function() -> str:
        """"""
        return generated.InterfaceWithStatic.static_function()


    @property
    def regular_property(self) -> str:
        """"""
        return self._native.regular_property

    @regular_property.setter
    def regular_property(self, value: str):
        self._native.regular_property = value


    @staticmethod
    def static_property() -> str:
        """"""
        return generated.InterfaceWithStatic.static_property()

