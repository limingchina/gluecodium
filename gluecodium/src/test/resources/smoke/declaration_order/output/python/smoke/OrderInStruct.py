

from smoke.NestedStruct import NestedStruct
from smoke.SomeEnum import SomeEnum

class OrderInStruct:
    """"""

    def __init__(self, native):
        self._native = native


    struct_field: NestedStruct


    enum_field: SomeEnum

