

from smoke.AnotherExternalStruct import AnotherExternalStruct
from smoke.ExternalStruct import ExternalStruct


from _native_base import _NativeBase

import generated


class Structs(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def get_external_struct() -> ExternalStruct:
        """"""
        native_result = generated.Structs.get_external_struct()
        return ExternalStruct(native_result)

    @staticmethod

    def get_another_external_struct() -> AnotherExternalStruct:
        """"""
        native_result = generated.Structs.get_another_external_struct()
        return AnotherExternalStruct(native_result)

