

import datetime

from _native_base import _NativeBase


class DurationDefaults(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    dayz: datetime.timedelta


    hourz: datetime.timedelta


    minutez: datetime.timedelta


    secondz: datetime.timedelta


    milliz: datetime.timedelta


    microz: datetime.timedelta


    nanoz: datetime.timedelta

