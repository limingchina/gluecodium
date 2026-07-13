

from smoke.DummyStruct import DummyStruct

class SkipFieldInPlatformImmutable:
    """"""

    def __init__(self, native):
        self._native = native


    int_field: int


    string_field: DummyStruct


    bool_field: bool

