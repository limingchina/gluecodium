

from smoke.DeclarationOrderWithFunctionsFieldStruct import DeclarationOrderWithFunctionsFieldStruct
from smoke.DeclarationOrderWithFunctionsFooBar import DeclarationOrderWithFunctionsFooBar
from smoke.DeclarationOrderWithFunctionsParameterStruct import DeclarationOrderWithFunctionsParameterStruct
from smoke.DeclarationOrderWithFunctionsReturnStruct import DeclarationOrderWithFunctionsReturnStruct
from smoke.DeclarationOrderWithFunctionsThrownStruct import DeclarationOrderWithFunctionsThrownStruct
import typing


from _native_base import _NativeBase

import generated


class DeclarationOrderWithFunctionsMainStructWithFunctions(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_DeclarationOrderWithFunctionsMainStructWithFunctions):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DeclarationOrderWithFunctionsMainStructWithFunctions(*[_unwrap(arg) for arg in args]))


    @property
    def struct_field(self) -> DeclarationOrderWithFunctionsFieldStruct:
        """"""
        return _wrap(self._native.struct_field, DeclarationOrderWithFunctionsFieldStruct)
    @struct_field.setter
    def struct_field(self, value: DeclarationOrderWithFunctionsFieldStruct):
      self._native.struct_field = _unwrap(value, DeclarationOrderWithFunctionsFieldStruct)


    def with_parameter(self, input: DeclarationOrderWithFunctionsParameterStruct): ...

    def with_return(self) -> DeclarationOrderWithFunctionsReturnStruct: ...

    def with_thrown(self): ...

