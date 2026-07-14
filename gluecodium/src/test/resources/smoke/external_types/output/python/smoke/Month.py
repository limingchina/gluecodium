

from __future__ import annotations


from enum import Enum

import generated


class Month(Enum):
    """"""

    JANUARY = generated.Month.JANUARY
    FEBRUARY = generated.Month.FEBRUARY
    MARCH = generated.Month.MARCH

    @property
    def _native(self):
        return self.value

