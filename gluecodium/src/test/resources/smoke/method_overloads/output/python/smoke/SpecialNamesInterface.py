

from __future__ import annotations

from smoke.Callback import Callback


from _native_base import _NativeBase

import generated


class SpecialNamesInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, SpecialNamesInterface):
            super().__init__(native)
        else:
            super().__init__(generated.SpecialNamesInterface())


    def dispatch(self, callback: Callback):
        """"""
        return self._native.dispatch(callback._native)

