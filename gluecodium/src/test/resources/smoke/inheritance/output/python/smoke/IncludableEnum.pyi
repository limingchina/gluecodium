

import typing

from enum import Enum

import generated


class IncludableEnum(Enum):
    """"""

    FOO = generated.smoke_IncludableEnum.FOO

    @property
    def _native(self):
        return self.value

