

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class EnumWithAlias(Enum):

    ONE = generated.smoke_EnumWithAlias.ONE
    TWO = generated.smoke_EnumWithAlias.TWO
    THREE = generated.smoke_EnumWithAlias.THREE
    FIRST = generated.smoke_EnumWithAlias.FIRST
    THE_BEST = generated.smoke_EnumWithAlias.THE_BEST

    @property
    def _native(self):
        return self.value

