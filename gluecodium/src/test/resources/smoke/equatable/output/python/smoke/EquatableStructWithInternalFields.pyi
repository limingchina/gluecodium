


from _native_base import _NativeBase


class EquatableStructWithInternalFields(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    public_field: str


    internal_field: str


    internal_list_field: list[str]


    internal_map_field: dict[str, str]


    internal_set_field: set[str]

