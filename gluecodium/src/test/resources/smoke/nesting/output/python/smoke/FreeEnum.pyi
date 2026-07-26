

import typing

from enum import Enum

import generated


class FreeEnum(Enum):
    """"""

    FOO = generated.smoke_FreeEnum.FOO
    BAR = generated.smoke_FreeEnum.BAR

    @property
    def _native(self):
        return self.value

