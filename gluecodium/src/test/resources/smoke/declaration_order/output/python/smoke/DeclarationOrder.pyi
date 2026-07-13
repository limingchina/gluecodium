

from smoke.NestedStruct import NestedStruct
from smoke.SomeEnum import SomeEnum
from smoke.dict[int, list[NestedStruct]] import dict[int, list[NestedStruct]]
from smoke.int import int
from smoke.list[NestedStruct] import list[NestedStruct]


from _native_base import _NativeBase

import generated


class DeclarationOrder(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], DeclarationOrder):
            super().__init__(args[0])
        else:
            super().__init__(generated.DeclarationOrder(*args))

from enum import Enum


class SomeEnum(Enum):
    """"""

    FOO = 0
    BAR = 1

