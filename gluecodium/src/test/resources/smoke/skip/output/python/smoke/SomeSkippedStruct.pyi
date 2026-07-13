


from _native_base import _NativeBase


class SomeSkippedStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    field: list[SomeSkippedEnum]

