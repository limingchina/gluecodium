

from __future__ import annotations

from smoke.ChildInterface import ChildInterface


from _native_base import _NativeBase

import generated


class GrandChildInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, GrandChildInterface):
            super().__init__(native)
        else:
            super().__init__(generated.GrandChildInterface())


    def grand_child_method(self):
        """"""
        return self._native.grand_child_method()

