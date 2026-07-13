

from smoke.datetime.datetime import datetime.datetime

from _native_base import _NativeBase


class DateDefaultsAliased(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    date_time: datetime.datetime


    date_time_utc: datetime.datetime


    before_epoch: datetime.datetime


    exactly_epoch: datetime.datetime

