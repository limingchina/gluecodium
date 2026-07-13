

import datetime

from _native_base import _NativeBase


class DurationInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def duration_function(self, input: datetime.timedelta) -> str:
        """"""
        return self._native.duration_function(input)

