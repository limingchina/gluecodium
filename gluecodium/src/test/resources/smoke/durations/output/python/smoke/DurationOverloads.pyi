

import datetime
import typing

from _native_base import _NativeBase

import generated


class DurationOverloads(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @typing.overload
    def duration_function(self, input: datetime.timedelta) -> str: ...

    @typing.overload
    def duration_function(self, input: str) -> str: ...

