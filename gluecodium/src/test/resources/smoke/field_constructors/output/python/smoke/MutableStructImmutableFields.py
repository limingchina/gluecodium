

from smoke.ImmutableStructNoClash import ImmutableStructNoClash

class MutableStructImmutableFields:
    """"""

    def __init__(self, native):
        self._native = native


    struct_field: ImmutableStructNoClash


    int_field: int


    bool_field: bool

