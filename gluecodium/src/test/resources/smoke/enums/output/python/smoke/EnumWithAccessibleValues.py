

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class EnumWithAccessibleValues(Enum):

    FOO = generated.smoke_EnumWithAccessibleValues.FOO
    BAR = generated.smoke_EnumWithAccessibleValues.BAR
    BAZ = generated.smoke_EnumWithAccessibleValues.BAZ
    FOO_ALIAS = generated.smoke_EnumWithAccessibleValues.FOO_ALIAS

    @property
    def _native(self):
        return self.value

