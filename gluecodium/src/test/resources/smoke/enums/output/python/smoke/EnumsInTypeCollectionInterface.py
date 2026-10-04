

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated

from smoke.EnumsInTypeCollection import EnumsInTypeCollection

class EnumsInTypeCollectionInterface(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def flip_enum_value(input: EnumsInTypeCollection.TCEnum) -> EnumsInTypeCollection.TCEnum:
        native_result = generated.smoke_EnumsInTypeCollectionInterface.flip_enum_value(_unwrap(input, EnumsInTypeCollection.TCEnum))
        return _get_or_create_wrapper(native_result, EnumsInTypeCollection.TCEnum)


