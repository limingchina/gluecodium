

from __future__ import annotations

from smoke.DeclarationOrderWithFunctionsFieldStruct import DeclarationOrderWithFunctionsFieldStruct
from smoke.DeclarationOrderWithFunctionsParameterStruct import DeclarationOrderWithFunctionsParameterStruct
from smoke.DeclarationOrderWithFunctionsReturnStruct import DeclarationOrderWithFunctionsReturnStruct
from smoke.DeclarationOrderWithFunctionsThrownStruct import DeclarationOrderWithFunctionsThrownStruct


from _native_base import _NativeBase

import generated


class DeclarationOrderWithFunctionsMainStructWithFunctions(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DeclarationOrderWithFunctionsMainStructWithFunctions):
            super().__init__(args[0])
        else:
            super().__init__(generated.DeclarationOrderWithFunctionsMainStructWithFunctions(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def struct_field(self) -> DeclarationOrderWithFunctionsFieldStruct:
        """"""
        return DeclarationOrderWithFunctionsFieldStruct(self._native.struct_field)
    @struct_field.setter
    def struct_field(self, value: DeclarationOrderWithFunctionsFieldStruct):
      self._native.struct_field = getattr(value, "_native", value)


    def with_parameter(self, input: DeclarationOrderWithFunctionsParameterStruct):
        """"""
        return self._native.with_parameter(input._native)

    def with_return(self) -> DeclarationOrderWithFunctionsReturnStruct:
        """"""
        return self._native.with_return()

    def with_thrown(self):
        """"""
        return self._native.with_thrown()

