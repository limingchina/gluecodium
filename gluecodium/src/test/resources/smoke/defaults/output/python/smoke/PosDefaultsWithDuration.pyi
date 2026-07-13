

import datetime

from _native_base import _NativeBase


class PosDefaultsWithDuration(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    duration_field: datetime.timedelta


    nanos_field: datetime.timedelta

