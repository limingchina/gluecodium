

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional


from enum import Enum

import generated


class FieldConstructorsNullableTypesFoodType(Enum):
    """"""

    VEGETABLES = generated.FieldConstructorsNullableTypesFoodType.VEGETABLES
    FRUITS = generated.FieldConstructorsNullableTypesFoodType.FRUITS

    @property
    def _native(self):
        return self.value

