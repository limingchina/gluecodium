

import typing

from enum import Enum

import generated


class EnumsVeryExternalEnum(Enum):
    """"""

    FOO = generated.smoke_EnumsVeryExternalEnum.FOO
    BAR = generated.smoke_EnumsVeryExternalEnum.BAR

    @property
    def _native(self):
        return self.value

