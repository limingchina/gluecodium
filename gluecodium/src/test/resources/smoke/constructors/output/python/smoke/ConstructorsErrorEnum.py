

from __future__ import annotations


from enum import Enum

import generated


class ConstructorsErrorEnum(Enum):
    """"""

    NONE = generated.ConstructorsErrorEnum.NONE
    CRASHED = generated.ConstructorsErrorEnum.CRASHED

    @property
    def _native(self):
        return self.value

