

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class ConstantsInterface(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    class StateEnum(Enum):
    
        OFF = generated.smoke_ConstantsInterfaceStateEnum.OFF
        ON = generated.smoke_ConstantsInterfaceStateEnum.ON
    
        @property
        def _native(self):
            return self.value
    
    

    BOOL_CONSTANT = True

    INT_CONSTANT = -11

    UINT_CONSTANT = 4294967295

    FLOAT_CONSTANT = 2.71

    DOUBLE_CONSTANT = -3.14

    STRING_CONSTANT = "Foo bar"

    ENUM_CONSTANT = StateEnum.ON

