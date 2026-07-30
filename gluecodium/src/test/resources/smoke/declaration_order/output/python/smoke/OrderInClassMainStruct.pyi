

from smoke.OrderInClassNestedStruct import OrderInClassNestedStruct
from smoke.OrderInClassSomeEnum import OrderInClassSomeEnum
import typing

class OrderInClassMainStruct:

    struct_field: OrderInClassNestedStruct

    type_def_field: int

    struct_array_field: list[OrderInClassNestedStruct]

    map_field: dict[int, list[OrderInClassNestedStruct]]

    enum_field: OrderInClassSomeEnum

