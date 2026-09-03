

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class AsyncErrorCode(Enum):

    VALUE1 = generated.smoke_AsyncErrorCode.VALUE1

    @property
    def _native(self):
        return self.value


