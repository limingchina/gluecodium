

from smoke.NestedStruct import NestedStruct
from smoke.SomeEnum import SomeEnum

class OrderInStructWithFunctions:
    """"""

    def __init__(self, native):
        self._native = native


    some_field: str


    def do_stuff(self, struct_foo: NestedStruct) -> SomeEnum:
        """"""
        return self._native.do_stuff(struct_foo)

