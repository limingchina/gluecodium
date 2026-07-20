

from __future__ import annotations


from enum import Enum

import generated


class ConstantsStateEnum(Enum):
    """"""

    OFF = generated.ConstantsStateEnum.OFF
    ON = generated.ConstantsStateEnum.ON

    @property
    def _native(self):
        return self.value

