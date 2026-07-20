

from smoke.EnumsInTypeCollectionTCEnum import EnumsInTypeCollectionTCEnum
import typing

from _native_base import _NativeBase

import generated


class EnumsInTypeCollectionInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def flip_enum_value(input: EnumsInTypeCollectionTCEnum) -> EnumsInTypeCollectionTCEnum: ...

