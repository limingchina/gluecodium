

from __future__ import annotations


from enum import Enum

import generated


class ExternalClassErrorEnum(Enum):
    """"""

    NONE = generated.ExternalClassErrorEnum.NONE
    CRASHED = generated.ExternalClassErrorEnum.CRASHED

    @property
    def _native(self):
        return self.value

