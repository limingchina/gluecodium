


from _native_base import _NativeBase


class EnumCollectionDefaultsExternal(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    list_field: list[ExternalEnum1]


    set_field: set[ExternalEnum2]


    map_field: dict[ExternalEnum3, ExternalEnum4]

