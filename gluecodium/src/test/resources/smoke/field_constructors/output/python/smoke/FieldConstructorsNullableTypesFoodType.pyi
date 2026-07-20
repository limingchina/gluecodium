

import typing

from enum import Enum

import generated


class FieldConstructorsNullableTypesFoodType(Enum):
    """"""

    VEGETABLES = generated.FieldConstructorsNullableTypesFoodType.VEGETABLES
    FRUITS = generated.FieldConstructorsNullableTypesFoodType.FRUITS

    @property
    def _native(self):
        return self.value

