

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from fire.SomeStruct import SomeStruct

class AmbiguousConstants(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    DUMMY = {42}


