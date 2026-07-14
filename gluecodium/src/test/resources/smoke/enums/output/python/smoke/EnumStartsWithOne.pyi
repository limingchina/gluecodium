


from enum import Enum

import generated


class EnumStartsWithOne(Enum):
    """"""

    FIRST = generated.EnumStartsWithOne.FIRST
    SECOND = generated.EnumStartsWithOne.SECOND

    @property
    def _native(self):
        return self.value

