

from smoke.NestedStruct import NestedStruct
from smoke.SomeEnum import SomeEnum

from _native_base import _NativeBase


class OrderInStructWithFunctions(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    some_field: str


    def do_stuff(self, struct_foo: NestedStruct) -> SomeEnum:
        """"""
        return self._native.do_stuff(struct_foo)

