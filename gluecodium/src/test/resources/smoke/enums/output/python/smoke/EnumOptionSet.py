

from __future__ import annotations


from enum import Enum

import generated


class EnumOptionSet(Enum):
    """"""

    ONE = generated.EnumOptionSet.ONE
    TWO = generated.EnumOptionSet.TWO
    THREE = generated.EnumOptionSet.THREE

    @property
    def _native(self):
        return self.value

