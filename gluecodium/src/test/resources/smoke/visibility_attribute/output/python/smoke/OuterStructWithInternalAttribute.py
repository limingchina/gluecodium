

from smoke.StructNestedInInternalStruct import StructNestedInInternalStruct

class OuterStructWithInternalAttribute:
    """"""

    def __init__(self, native):
        self._native = native


    inner: StructNestedInInternalStruct

