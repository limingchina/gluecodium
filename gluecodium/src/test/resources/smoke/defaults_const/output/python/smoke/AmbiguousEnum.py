

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class AmbiguousEnum(Enum):

    DISABLED = generated.smoke_AmbiguousEnum.DISABLED

    @property
    def _native(self):
        return self.value


