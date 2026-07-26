

import typing

from enum import Enum

import generated


class DontSmokeEnum(Enum):
    """"""

    FOO = generated.dont_smoke_DontSmokeEnum.FOO

    @property
    def _native(self):
        return self.value

