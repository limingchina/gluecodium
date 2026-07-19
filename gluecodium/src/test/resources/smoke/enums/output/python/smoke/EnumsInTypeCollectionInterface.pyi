

from smoke.EnumsInTypeCollectionTCEnum import EnumsInTypeCollectionTCEnum

from _native_base import _NativeBase

import generated


class EnumsInTypeCollectionInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def flip_enum_value(input: EnumsInTypeCollectionTCEnum) -> EnumsInTypeCollectionTCEnum:
        """"""
        native_result = generated.EnumsInTypeCollectionInterface.flip_enum_value(input._native)
        return EnumsInTypeCollectionTCEnum(native_result)

