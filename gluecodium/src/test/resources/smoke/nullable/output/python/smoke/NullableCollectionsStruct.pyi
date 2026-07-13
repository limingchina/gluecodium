


from _native_base import _NativeBase


class NullableCollectionsStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    dates: list[Optional[datetime.datetime]]


    structs: dict[int, Optional[SomeStruct]]

