

from fire.AmbiguousEnum import AmbiguousEnum
from fire.SomeStruct import SomeStruct

from _native_base import _NativeBase


class AmbiguousDefaults(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    field1: AmbiguousEnum


    field2: SomeStruct

