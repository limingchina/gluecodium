

from __future__ import annotations



from _native_base import _NativeBase

import generated


class ExposeInternalInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ExposeInternalInterface):
            super().__init__(native)
        else:
            super().__init__(generated.ExposeInternalInterface())

