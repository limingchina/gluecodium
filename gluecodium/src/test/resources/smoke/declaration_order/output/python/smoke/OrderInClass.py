

from smoke.NestedStruct import NestedStruct
from smoke.SomeEnum import SomeEnum
from smoke.dict[int, list[NestedStruct]] import dict[int, list[NestedStruct]]
from smoke.int import int
from smoke.list[NestedStruct] import list[NestedStruct]

class OrderInClass:
    """"""

    def __init__(self, native):
        self._native = native

