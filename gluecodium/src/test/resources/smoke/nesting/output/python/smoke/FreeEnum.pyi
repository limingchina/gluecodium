

import typing

from enum import Enum

import generated


class FreeEnum(Enum):
    """"""

    FOO = generated.FreeEnum.FOO
    BAR = generated.FreeEnum.BAR

    @property
    def _native(self):
        return self.value

