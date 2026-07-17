

from __future__ import annotations


from enum import Enum

import generated


class FoodType(Enum):
    """"""

    VEGETABLES = generated.FoodType.VEGETABLES
    FRUITS = generated.FoodType.FRUITS

    @property
    def _native(self):
        return self.value

