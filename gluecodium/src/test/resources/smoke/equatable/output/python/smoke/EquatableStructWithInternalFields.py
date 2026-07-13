


class EquatableStructWithInternalFields:
    """"""

    def __init__(self, native):
        self._native = native


    public_field: str


    internal_field: str


    internal_list_field: list[str]


    internal_map_field: dict[str, str]


    internal_set_field: set[str]

