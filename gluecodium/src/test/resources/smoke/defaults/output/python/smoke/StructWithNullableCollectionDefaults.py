


class StructWithNullableCollectionDefaults:
    """"""

    def __init__(self, native):
        self._native = native


    nullable_list_field: Optional[list[str]]


    nullable_map_field: Optional[dict[str, str]]


    nullable_set_field: Optional[set[str]]

