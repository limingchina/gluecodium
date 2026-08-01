

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class FreeEnum(Enum):

    FOO = generated.smoke_FreeEnum.FOO
    BAR = generated.smoke_FreeEnum.BAR

    @property
    def _native(self):
        return self.value


