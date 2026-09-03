

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class Persistence(Enum):

    NONE = generated.smoke_Persistence.NONE
    FOR_SESSION = generated.smoke_Persistence.FOR_SESSION
    PERMANENT = generated.smoke_Persistence.PERMANENT

    @property
    def _native(self):
        return self.value


