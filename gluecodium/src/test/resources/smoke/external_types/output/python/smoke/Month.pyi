

import typing

from enum import Enum

import generated


class Month(Enum):
    """"""

    JANUARY = generated.smoke_Month.JANUARY
    FEBRUARY = generated.smoke_Month.FEBRUARY
    MARCH = generated.smoke_Month.MARCH

    @property
    def _native(self):
        return self.value

