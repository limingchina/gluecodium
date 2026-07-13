

from __future__ import annotations

from smoke.FooChecker import FooChecker


from _native_base import _NativeBase

import generated


class InterfaceInInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, InterfaceInInterface):
            super().__init__(native)
        else:
            super().__init__(generated.InterfaceInInterface())

