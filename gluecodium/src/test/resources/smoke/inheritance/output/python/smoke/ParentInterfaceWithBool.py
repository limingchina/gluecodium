

from __future__ import annotations



from _native_base import _NativeBase

import generated


class ParentInterfaceWithBool(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ParentInterfaceWithBool):
            super().__init__(native)
        else:
            super().__init__(generated.ParentInterfaceWithBool())


    def root_method(self, input1: bool):
        """"""
        return self._native.root_method(input1)

