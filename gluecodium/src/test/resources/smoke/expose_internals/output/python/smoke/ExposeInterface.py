

from __future__ import annotations



from _native_base import _NativeBase

import generated


class ExposeInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ExposeInterface):
            super().__init__(native)
        else:
            super().__init__(generated.ExposeInterface())

