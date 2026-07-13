

from smoke.TCEnum import TCEnum

from _native_base import _NativeBase


class EnumsInTypeCollectionInterface(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def flip_enum_value(self, input: TCEnum) -> TCEnum:
        """"""
        return self._native.flip_enum_value(input)

