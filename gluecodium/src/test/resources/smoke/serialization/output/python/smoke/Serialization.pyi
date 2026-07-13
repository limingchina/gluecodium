

from smoke.NestedSerializableStruct import NestedSerializableStruct
from smoke.SomeEnum import SomeEnum
from smoke.dict[int, str] import dict[int, str]
from smoke.list[NestedSerializableStruct] import list[NestedSerializableStruct]

from _native_base import _NativeBase


class Serialization(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

