

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class LevelOneLevelTwoLevelThreeLevelFourEnum(Enum):

    NONE = generated.smoke_LevelOneLevelTwoLevelThreeLevelFourEnum.NONE

    @property
    def _native(self):
        return self.value

