

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.ClassWithOverloads import ClassWithOverloads
from smoke.Enums import Enums
from smoke.Structs import Structs

class UseCppExternalTypes(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def use_struct(input: Structs.AnotherExternalStruct):
        generated.dontsmoke_UseCppExternalTypes.use_struct(_unwrap(input, Structs.AnotherExternalStruct))

    @staticmethod
    def use_enum(input: Enums.ExternalEnum):
        generated.dontsmoke_UseCppExternalTypes.use_enum(_unwrap(input, Enums.ExternalEnum))

    @staticmethod
    def use_class(input: ClassWithOverloads):
        generated.dontsmoke_UseCppExternalTypes.use_class(_unwrap(input, ClassWithOverloads))


