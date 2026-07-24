

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class DartSeason(Enum):
    """"""

    WINTER = generated.DartSeason.WINTER
    SPRING = generated.DartSeason.SPRING
    SUMMER = generated.DartSeason.SUMMER
    AUTUMN = generated.DartSeason.AUTUMN

    @property
    def _native(self):
        return self.value

