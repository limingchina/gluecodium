

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class Season(Enum):

    WINTER = generated.smoke_Season.WINTER
    SPRING = generated.smoke_Season.SPRING
    SUMMER = generated.smoke_Season.SUMMER
    AUTUMN = generated.smoke_Season.AUTUMN

    @property
    def _native(self):
        return self.value

