

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class Enums(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def method_with_external_enum(input: Enums.ExternalEnum):
        generated.smoke_Enums.method_with_external_enum(_unwrap(input, Enums.ExternalEnum))

    class ExternalEnum(Enum):
    
        FOO_VALUE = 0
        BAR_VALUE = 1
    
    
    
    class VeryExternalEnum(Enum):
    
        FOO = 0
        BAR = 1
    
    

