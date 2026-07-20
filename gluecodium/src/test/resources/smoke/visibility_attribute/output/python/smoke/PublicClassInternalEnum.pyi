

import typing

from enum import Enum

import generated


class PublicClassInternalEnum(Enum):
    """"""

    FOO = generated.PublicClassInternalEnum.FOO
    BAR = generated.PublicClassInternalEnum.BAR

    @property
    def _native(self):
        return self.value

