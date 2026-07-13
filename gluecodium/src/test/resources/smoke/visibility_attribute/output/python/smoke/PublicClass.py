

from smoke.InternalStruct import InternalStruct

class PublicClass:
    """"""

    def __init__(self, native):
        self._native = native


    def internal_method(self, input: InternalStruct) -> InternalStruct:
        """"""
        return self._native.internal_method(input)


    @property
    def internal_struct_property(self) -> InternalStruct:
        """"""
        return self._native.internal_struct_property


