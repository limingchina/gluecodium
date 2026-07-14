

from __future__ import annotations

from smoke.StructsAnotherExternalStruct import StructsAnotherExternalStruct
from smoke.StructsExternalStruct import StructsExternalStruct


from _native_base import _NativeBase

import generated


class Structs(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def get_external_struct() -> StructsExternalStruct:
        """"""
        native_result = generated.Structs.get_external_struct()
        return StructsExternalStruct(native_result)

    @staticmethod
    def get_another_external_struct() -> StructsAnotherExternalStruct:
        """"""
        native_result = generated.Structs.get_another_external_struct()
        return StructsAnotherExternalStruct(native_result)

