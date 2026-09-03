

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated


class EnumWithAliasWithDeprecated(Enum):

    ONE = generated.smoke_EnumWithAliasWithDeprecated.ONE
    TWO = generated.smoke_EnumWithAliasWithDeprecated.TWO
    THREE = generated.smoke_EnumWithAliasWithDeprecated.THREE
    FIRST = generated.smoke_EnumWithAliasWithDeprecated.FIRST

    @property
    def _native(self):
        return self.value


