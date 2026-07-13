

from smoke.ImmutableStructWithDefaults import ImmutableStructWithDefaults

class PosDefaultStructWithFieldUsingImmutableStruct:
    """"""

    def __init__(self, native):
        self._native = native


    some_field1: ImmutableStructWithDefaults

