


from _native_base import _NativeBase


class StructWithJavaPositionalDefaults(_NativeBase):
    """Foo Bar this is a comment"""

    def __init__(self, native):
        super().__init__(native)

    first init!
    first_init_field: int

    first free!
    first_free_field: str

    second init yeah!
    second_init_field: float

    second free here!
    second_free_field: bool

    third should be last!
    third_init_field: str

