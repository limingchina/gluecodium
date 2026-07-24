

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.DeclarationOrderWithFunctionsFieldStruct import DeclarationOrderWithFunctionsFieldStruct
from smoke.DeclarationOrderWithFunctionsFooBar import DeclarationOrderWithFunctionsFooBar
from smoke.DeclarationOrderWithFunctionsParameterStruct import DeclarationOrderWithFunctionsParameterStruct
from smoke.DeclarationOrderWithFunctionsReturnStruct import DeclarationOrderWithFunctionsReturnStruct
from smoke.DeclarationOrderWithFunctionsThrownStruct import DeclarationOrderWithFunctionsThrownStruct


from _native_base import _NativeBase

import generated


class DeclarationOrderWithFunctions(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.DeclarationOrderWithFunctions):
            super().__init__(args[0])
        else:
            super().__init__(generated.DeclarationOrderWithFunctions(*[_unwrap(arg) for arg in args]))

