

from smoke.FieldCustomConstructorsMix import FieldCustomConstructorsMix

from _native_base import _NativeBase


class FieldCustomConstructorsMix(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    string_field: str


    int_field: int


    bool_field: bool


    def create_me(self, int_value: int, dummy: float) -> FieldCustomConstructorsMix:
        """"""
        return self._native.create_me(int_value, dummy)

