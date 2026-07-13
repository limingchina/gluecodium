


class NullableCollectionsStruct:
    """"""

    def __init__(self, native):
        self._native = native


    dates: list[Optional[datetime.datetime]]


    structs: dict[int, Optional[SomeStruct]]

