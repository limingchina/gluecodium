

from smoke.FreeEnum import FreeEnum
from smoke.FreeError import FreeError
from smoke.FreePoint import FreePoint
from smoke.datetime.datetime import datetime.datetime

class UseFreeTypes:
    """"""

    def __init__(self, native):
        self._native = native


    def do_stuff(self, point: FreePoint, mode: FreeEnum) -> datetime.datetime:
        """"""
        return self._native.do_stuff(point, mode)

