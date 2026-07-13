


class PublicStructWithNonDefaultInternalField:
    """"""

    def __init__(self, native):
        self._native = native


    defaulted_field: int


    internal_field: str


    public_field: bool

