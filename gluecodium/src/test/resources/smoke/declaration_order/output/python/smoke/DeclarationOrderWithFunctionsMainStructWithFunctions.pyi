

from smoke.DeclarationOrderWithFunctionsFieldStruct import DeclarationOrderWithFunctionsFieldStruct
from smoke.DeclarationOrderWithFunctionsFooBar import DeclarationOrderWithFunctionsFooBar
from smoke.DeclarationOrderWithFunctionsParameterStruct import DeclarationOrderWithFunctionsParameterStruct
from smoke.DeclarationOrderWithFunctionsReturnStruct import DeclarationOrderWithFunctionsReturnStruct
from smoke.DeclarationOrderWithFunctionsThrownStruct import DeclarationOrderWithFunctionsThrownStruct
import typing

class DeclarationOrderWithFunctionsMainStructWithFunctions:

    struct_field: DeclarationOrderWithFunctionsFieldStruct

    def with_parameter(self, input: DeclarationOrderWithFunctionsParameterStruct):
        ...

    def with_return(self) -> DeclarationOrderWithFunctionsReturnStruct:
        ...

    def with_thrown(self):
        ...

