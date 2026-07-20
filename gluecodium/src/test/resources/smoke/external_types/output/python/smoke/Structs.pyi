

from smoke.StructsAnotherExternalStruct import StructsAnotherExternalStruct
from smoke.StructsExternalStruct import StructsExternalStruct
import typing

from _native_base import _NativeBase

import generated


class Structs(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def get_external_struct() -> StructsExternalStruct: ...

    @staticmethod
    def get_another_external_struct() -> StructsAnotherExternalStruct: ...

