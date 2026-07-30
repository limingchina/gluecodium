

from smoke.OrderInStructWithFunctionsNestedStruct import OrderInStructWithFunctionsNestedStruct
from smoke.OrderInStructWithFunctionsSomeEnum import OrderInStructWithFunctionsSomeEnum
import typing

class OrderInStructWithFunctions:

    some_field: str

    def do_stuff(self, struct_foo: OrderInStructWithFunctionsNestedStruct) -> OrderInStructWithFunctionsSomeEnum:
        ...

