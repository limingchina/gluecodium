


from _native_base import _NativeBase


class EnumCollectionDefaults(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    list_field: list[Enum1]


    set_field: set[Enum2]


    map_field: dict[Enum3, Enum4]

