

from smoke.Builder import Builder
from smoke.InnerEnum import InnerEnum
from smoke.InstantiationError import InstantiationError
from smoke.OuterStruct import OuterStruct

class OuterStruct:
    """"""

    def __init__(self, native):
        self._native = native


    field: str


    def do_nothing(self):
        """"""
        return self._native.do_nothing()

