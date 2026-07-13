

from __future__ import annotations

from smoke.NestedSerializableStruct import NestedSerializableStruct
from smoke.SomeEnum import SomeEnum
from smoke.dict[int, str] import dict[int, str]
from smoke.list[NestedSerializableStruct] import list[NestedSerializableStruct]


from _native_base import _NativeBase

import generated


class Serialization(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Serialization):
            super().__init__(args[0])
        else:
            super().__init__(generated.Serialization(*args))

from enum import Enum


class SomeEnum(Enum):
    """"""

    FOO = 0
    BAR = 1

