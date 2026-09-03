

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class EnumOptionSetComments(Enum):

    ONE = generated.smoke_EnumOptionSetComments.ONE
    TWO = generated.smoke_EnumOptionSetComments.TWO
    THREE = generated.smoke_EnumOptionSetComments.THREE

    @property
    def _native(self):
        return self.value


