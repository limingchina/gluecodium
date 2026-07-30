

from smoke.DeclarationOrderNestedStruct import DeclarationOrderNestedStruct
from smoke.DeclarationOrderSomeEnum import DeclarationOrderSomeEnum
import typing

class DeclarationOrderMainStruct:

    struct_field: DeclarationOrderNestedStruct

    type_def_field: int

    struct_array_field: list[DeclarationOrderNestedStruct]

    map_field: dict[int, list[DeclarationOrderNestedStruct]]

    enum_field: DeclarationOrderSomeEnum

