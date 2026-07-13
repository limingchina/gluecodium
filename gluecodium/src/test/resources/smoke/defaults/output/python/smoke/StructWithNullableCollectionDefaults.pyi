


from _native_base import _NativeBase


class StructWithNullableCollectionDefaults(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    nullable_list_field: Optional[list[str]]


    nullable_map_field: Optional[dict[str, str]]


    nullable_set_field: Optional[set[str]]

