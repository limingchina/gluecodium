


from _native_base import _NativeBase


class UseEnumOptionSet(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    set_field: set[EnumOptionSet]


    set_field_empty: set[EnumOptionSet]


    set_field_value: set[EnumOptionSet]


    def round_trip(self, input: set[EnumOptionSet]) -> set[EnumOptionSet]:
        """"""
        return self._native.round_trip(input)

