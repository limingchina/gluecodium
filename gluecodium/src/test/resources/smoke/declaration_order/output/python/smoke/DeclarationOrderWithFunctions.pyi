

from smoke.FieldStruct import FieldStruct
from smoke.FooBarError import FooBarError
from smoke.ParameterStruct import ParameterStruct
from smoke.ReturnStruct import ReturnStruct
from smoke.ThrownStruct import ThrownStruct


from _native_base import _NativeBase

import generated


class DeclarationOrderWithFunctions(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], DeclarationOrderWithFunctions):
            super().__init__(args[0])
        else:
            super().__init__(generated.DeclarationOrderWithFunctions(*args))

