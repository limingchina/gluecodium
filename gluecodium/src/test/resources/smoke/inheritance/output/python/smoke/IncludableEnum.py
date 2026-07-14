

from __future__ import annotations


from enum import Enum

import generated


class IncludableEnum(Enum):
    """"""

    FOO = generated.IncludableEnum.FOO

    @property
    def _native(self):
        return self.value

