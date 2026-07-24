

import typing

from enum import Enum

import generated


class EnumsVeryExternalEnum(Enum):
    """"""

    FOO = generated.EnumsVeryExternalEnum.FOO
    BAR = generated.EnumsVeryExternalEnum.BAR

    @property
    def _native(self):
        return self.value

