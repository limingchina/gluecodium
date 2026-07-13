

from smoke.TCEnum import TCEnum


from _native_base import _NativeBase

import generated


class EnumsInTypeCollectionInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def flip_enum_value(input: TCEnum) -> TCEnum:
        """"""
        native_result = generated.EnumsInTypeCollectionInterface.flip_enum_value(input)
        return TCEnum(native_result)

