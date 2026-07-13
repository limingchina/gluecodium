


from _native_base import _NativeBase


class StructWithCollectionDefaults(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    empty_list_field: list[str]


    empty_map_field: dict[str, str]


    empty_set_field: set[str]


    list_field: list[str]


    map_field: dict[str, str]


    set_field: set[str]

