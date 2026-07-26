

import typing

from enum import Enum

import generated


class ConstructorsErrorEnum(Enum):
    """"""

    NONE = generated.smoke_ConstructorsErrorEnum.NONE
    CRASHED = generated.smoke_ConstructorsErrorEnum.CRASHED

    @property
    def _native(self):
        return self.value

