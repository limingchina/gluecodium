

import datetime
from smoke.FreeEnum import FreeEnum
from smoke.FreePoint import FreePoint

from _native_base import _NativeBase

import generated


class UseFreeTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def do_stuff(self, point: FreePoint, mode: FreeEnum) -> datetime.datetime:
        """"""
        return self._native.do_stuff(point._native, mode._native)

