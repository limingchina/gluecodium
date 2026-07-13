

from smoke.FreeEnum import FreeEnum
from smoke.FreeError import FreeError
from smoke.FreePoint import FreePoint
from smoke.datetime.datetime import datetime.datetime

from _native_base import _NativeBase


class UseFreeTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def do_stuff(self, point: FreePoint, mode: FreeEnum) -> datetime.datetime:
        """"""
        return self._native.do_stuff(point, mode)

