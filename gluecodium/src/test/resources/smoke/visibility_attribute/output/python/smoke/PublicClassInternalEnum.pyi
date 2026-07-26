

import typing

from enum import Enum

import generated


class PublicClassInternalEnum(Enum):
    """"""

    FOO = generated.smoke_PublicClassInternalEnum.FOO
    BAR = generated.smoke_PublicClassInternalEnum.BAR

    @property
    def _native(self):
        return self.value

