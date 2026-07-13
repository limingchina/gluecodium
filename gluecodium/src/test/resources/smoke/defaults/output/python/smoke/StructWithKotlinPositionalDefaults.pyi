


from _native_base import _NativeBase


class StructWithKotlinPositionalDefaults(_NativeBase):
    """This is an important struct that uses positional default annotation."""

    def __init__(self, native):
        super().__init__(native)


    first_init_field: int


    first_free_field: str


    second_init_field: float


    second_free_field: bool


    third_init_field: str

