

from smoke.DeclarationOrderNestedStruct import DeclarationOrderNestedStruct
from smoke.SomeEnum import SomeEnum


from _native_base import _NativeBase

import generated


class DeclarationOrder(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], DeclarationOrder):
            super().__init__(args[0])
        else:
            super().__init__(generated.DeclarationOrder(*[getattr(arg, "_native", arg) for arg in args]))
from enum import Enum


class SomeEnum(Enum):
    """"""

    FOO = 0
    BAR = 1


