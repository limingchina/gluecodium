

from smoke.NestedSerializableStruct import NestedSerializableStruct
from smoke.SomeEnum import SomeEnum
from smoke.dict[int, str] import dict[int, str]
from smoke.list[NestedSerializableStruct] import list[NestedSerializableStruct]

class Serialization:
    """"""

    def __init__(self, native):
        self._native = native

