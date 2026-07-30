

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.DeclarationOrderWithFunctionsFieldStruct import DeclarationOrderWithFunctionsFieldStruct
from smoke.DeclarationOrderWithFunctionsFooBar import DeclarationOrderWithFunctionsFooBar
from smoke.DeclarationOrderWithFunctionsParameterStruct import DeclarationOrderWithFunctionsParameterStruct
from smoke.DeclarationOrderWithFunctionsReturnStruct import DeclarationOrderWithFunctionsReturnStruct
from smoke.DeclarationOrderWithFunctionsThrownStruct import DeclarationOrderWithFunctionsThrownStruct


from _native_base import _NativeBase

import generated


class DeclarationOrderWithFunctionsMainStructWithFunctions(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_DeclarationOrderWithFunctionsMainStructWithFunctions):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_DeclarationOrderWithFunctionsMainStructWithFunctions(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    @property
    def struct_field(self) -> DeclarationOrderWithFunctionsFieldStruct:
        return _wrap(self._native.struct_field, DeclarationOrderWithFunctionsFieldStruct)
    @struct_field.setter
    def struct_field(self, value: DeclarationOrderWithFunctionsFieldStruct):
      self._native.struct_field = _unwrap(value, DeclarationOrderWithFunctionsFieldStruct)


    def with_parameter(self, input: DeclarationOrderWithFunctionsParameterStruct):
        return _wrap(self._native.with_parameter(_unwrap(input, DeclarationOrderWithFunctionsParameterStruct)), None)

    def with_return(self) -> DeclarationOrderWithFunctionsReturnStruct:
        return _wrap(self._native.with_return(), DeclarationOrderWithFunctionsReturnStruct)

    def with_thrown(self):
        return _wrap(self._native.with_thrown(), None)

