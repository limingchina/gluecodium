

from __future__ import annotations

import datetime


from _native_base import _NativeBase

import generated


class DurationInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, DurationInterface):
            super().__init__(native)
        else:
            super().__init__(generated.DurationInterface())


    def duration_function(self, input: datetime.timedelta) -> str:
        """"""
        return self._native.duration_function(input)

