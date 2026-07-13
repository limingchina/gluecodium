


class UseEnumOptionSet:
    """"""

    def __init__(self, native):
        self._native = native


    set_field: set[EnumOptionSet]


    set_field_empty: set[EnumOptionSet]


    set_field_value: set[EnumOptionSet]


    def round_trip(self, input: set[EnumOptionSet]) -> set[EnumOptionSet]:
        """"""
        return self._native.round_trip(input)

