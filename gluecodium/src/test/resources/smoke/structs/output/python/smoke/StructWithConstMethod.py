


class StructWithConstMethod:
    """"""

    def __init__(self, native):
        self._native = native


    string_field: str


    def double_const(self) -> float:
        """"""
        return self._native.double_const()

