


from enum import Enum

import generated


class EnumWithAlias(Enum):
    """"""

    ONE = generated.EnumWithAlias.ONE
    TWO = generated.EnumWithAlias.TWO
    THREE = generated.EnumWithAlias.THREE
    FIRST = generated.EnumWithAlias.FIRST
    THE_BEST = generated.EnumWithAlias.THE_BEST

    @property
    def _native(self):
        return self.value

