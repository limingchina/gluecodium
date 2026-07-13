

from __future__ import annotations



from _native_base import _NativeBase

import generated


class CalculationResult(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, CalculationResult):
            super().__init__(native)
        else:
            super().__init__(generated.CalculationResult())

