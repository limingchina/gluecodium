

from __future__ import annotations



from _native_base import _NativeBase

import generated


class InternalInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, InternalInterface):
            super().__init__(native)
        else:
            super().__init__(generated.InternalInterface())

    def foo_bar(self):
        """"""
        return self._native.foo_bar()


    @staticmethod
    def some_property_of_internal_interface() -> str:
        """"""
        return generated.InternalInterface.some_property_of_internal_interface()

