

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

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
        native_result = generated.smoke_Structs.get_external_struct()
        return _get_or_create_wrapper(native_result, StructsExternalStruct)

    @staticmethod
    def get_another_external_struct() -> StructsAnotherExternalStruct:
        """"""
        native_result = generated.smoke_Structs.get_another_external_struct()
        return _get_or_create_wrapper(native_result, StructsAnotherExternalStruct)

