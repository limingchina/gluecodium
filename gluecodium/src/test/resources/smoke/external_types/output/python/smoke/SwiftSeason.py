

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class SwiftSeason(Enum):
    """"""

    WINTER = generated.smoke_SwiftSeason.WINTER
    SPRING = generated.smoke_SwiftSeason.SPRING
    SUMMER = generated.smoke_SwiftSeason.SUMMER
    AUTUMN = generated.smoke_SwiftSeason.AUTUMN

    @property
    def _native(self):
        return self.value

