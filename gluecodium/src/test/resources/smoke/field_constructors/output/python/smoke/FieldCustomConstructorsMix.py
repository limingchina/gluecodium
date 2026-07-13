

from smoke.FieldCustomConstructorsMix import FieldCustomConstructorsMix

class FieldCustomConstructorsMix:
    """"""

    def __init__(self, native):
        self._native = native


    string_field: str


    int_field: int


    bool_field: bool


    def create_me(self, int_value: int, dummy: float) -> FieldCustomConstructorsMix:
        """"""
        return self._native.create_me(int_value, dummy)

