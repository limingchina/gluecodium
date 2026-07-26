

import typing

from enum import Enum

import generated


class Month(Enum):
    """"""

    JANUARY = generated.kotlin_smoke_Month.JANUARY
    FEBRUARY = generated.kotlin_smoke_Month.FEBRUARY
    MARCH = generated.kotlin_smoke_Month.MARCH

    @property
    def _native(self):
        return self.value

