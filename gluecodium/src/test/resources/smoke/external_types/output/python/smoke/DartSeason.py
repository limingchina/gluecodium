

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class DartSeason(Enum):
    """"""

    WINTER = generated.smoke_DartSeason.WINTER
    SPRING = generated.smoke_DartSeason.SPRING
    SUMMER = generated.smoke_DartSeason.SUMMER
    AUTUMN = generated.smoke_DartSeason.AUTUMN

    @property
    def _native(self):
        return self.value

