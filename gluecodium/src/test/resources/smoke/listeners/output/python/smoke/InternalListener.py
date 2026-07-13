

from __future__ import annotations



from _native_base import _NativeBase

import generated


class InternalListener(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, InternalListener):
            super().__init__(native)
        else:
            super().__init__(generated.InternalListener())


    def on_event(self):
        """"""
        return self._native.on_event()

