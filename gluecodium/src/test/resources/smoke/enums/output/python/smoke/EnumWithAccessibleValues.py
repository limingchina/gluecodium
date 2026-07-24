

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class EnumWithAccessibleValues(Enum):
    """"""

    FOO = generated.EnumWithAccessibleValues.FOO
    BAR = generated.EnumWithAccessibleValues.BAR
    BAZ = generated.EnumWithAccessibleValues.BAZ
    FOO_ALIAS = generated.EnumWithAccessibleValues.FOO_ALIAS

    @property
    def _native(self):
        return self.value

