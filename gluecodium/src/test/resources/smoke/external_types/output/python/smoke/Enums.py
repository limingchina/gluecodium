

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
    
        FOO_VALUE = generated.smoke_Enums.ExternalEnum.FOO_VALUE
        BAR_VALUE = generated.smoke_Enums.ExternalEnum.BAR_VALUE
    
        @property
        def _native(self):
            return self.value
    
    
    
    class VeryExternalEnum(Enum):
    
        FOO = generated.smoke_Enums.VeryExternalEnum.FOO
        BAR = generated.smoke_Enums.VeryExternalEnum.BAR
    
        @property
        def _native(self):
            return self.value
    
    

