

import typing

from enum import Enum

import generated


class SomethingEnum(Enum):
    """"""

    REALLY_FIRST = generated.smoke_SomethingEnum.REALLY_FIRST
    EXPLICIT = generated.smoke_SomethingEnum.EXPLICIT
    LAST = generated.smoke_SomethingEnum.LAST

    @property
    def _native(self):
        return self.value

