

from smoke.ImmutableDefaultCtor import ImmutableDefaultCtor

class MutableStructImmutableFieldsDefault:
    """"""

    def __init__(self, native):
        self._native = native


    struct_field: ImmutableDefaultCtor


    int_field: int


    bool_field: bool

