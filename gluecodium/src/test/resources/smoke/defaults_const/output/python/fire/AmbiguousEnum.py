

from __future__ import annotations


from enum import Enum

import generated


class AmbiguousEnum(Enum):
    """"""

    DISABLED = generated.AmbiguousEnum.DISABLED

    @property
    def _native(self):
        return self.value

