


class EnumCollectionDefaultsExternal:
    """"""

    def __init__(self, native):
        self._native = native


    list_field: list[ExternalEnum1]


    set_field: set[ExternalEnum2]


    map_field: dict[ExternalEnum3, ExternalEnum4]

