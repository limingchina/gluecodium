

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class EnumWithAliasWithDeprecated(Enum):
    """"""

    ONE = generated.smoke_EnumWithAliasWithDeprecated.ONE
    TWO = generated.smoke_EnumWithAliasWithDeprecated.TWO
    THREE = generated.smoke_EnumWithAliasWithDeprecated.THREE
    FIRST = generated.smoke_EnumWithAliasWithDeprecated.FIRST

    @property
    def _native(self):
        return self.value

