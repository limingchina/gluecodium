

from smoke.NestedStruct import NestedStruct
from smoke.SomeEnum import SomeEnum


from _native_base import _NativeBase

import generated


class OrderInStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], OrderInStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.OrderInStruct(*args))


    @property
    def struct_field(self) -> NestedStruct:
        """"""
        return self._native.struct_field

    @struct_field.setter
    def struct_field(self, value: NestedStruct):
        self._native.struct_field = value



    @property
    def enum_field(self) -> SomeEnum:
        """"""
        return self._native.enum_field

    @enum_field.setter
    def enum_field(self, value: SomeEnum):
        self._native.enum_field = value


