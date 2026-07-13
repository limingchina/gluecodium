

import datetime

from _native_base import _NativeBase


class DateInterval(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    start: datetime.datetime


    end: datetime.datetime

