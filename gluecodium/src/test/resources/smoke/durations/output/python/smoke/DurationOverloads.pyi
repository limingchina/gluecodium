

import datetime

from _native_base import _NativeBase


class DurationOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def duration_function(self, input: datetime.timedelta) -> str:
        """"""
        return self._native.duration_function(input)


    def duration_function(self, input: str) -> str:
        """"""
        return self._native.duration_function(input)

