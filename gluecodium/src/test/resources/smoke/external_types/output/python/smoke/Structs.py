

from smoke.AnotherExternalStruct import AnotherExternalStruct
from smoke.ExternalStruct import ExternalStruct

class Structs:
    """"""

    def __init__(self, native):
        self._native = native


    def get_external_struct(self) -> ExternalStruct:
        """"""
        return self._native.get_external_struct()


    def get_another_external_struct(self) -> AnotherExternalStruct:
        """"""
        return self._native.get_another_external_struct()

