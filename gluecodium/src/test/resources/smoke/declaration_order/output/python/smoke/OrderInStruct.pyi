

from smoke.NestedStruct import NestedStruct
from smoke.SomeEnum import SomeEnum

from _native_base import _NativeBase


class OrderInStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    struct_field: NestedStruct


    enum_field: SomeEnum

