

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class SwiftSeason(Enum):
    """"""

    WINTER = generated.SwiftSeason.WINTER
    SPRING = generated.SwiftSeason.SPRING
    SUMMER = generated.SwiftSeason.SUMMER
    AUTUMN = generated.SwiftSeason.AUTUMN

    @property
    def _native(self):
        return self.value

