

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class Constants(_NativeBase):
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_Constants):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_Constants(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))

    class StateEnum(Enum):
    
        OFF = generated.smoke_Constants.StateEnum.OFF
        ON = generated.smoke_Constants.StateEnum.ON
    
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

