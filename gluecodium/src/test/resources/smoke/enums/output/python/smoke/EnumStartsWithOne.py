

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class EnumStartsWithOne(Enum):

    FIRST = generated.smoke_EnumStartsWithOne.FIRST
    SECOND = generated.smoke_EnumStartsWithOne.SECOND

    @property
    def _native(self):
        return self.value


