

import typing

from enum import Enum

import generated


class StandaloneExternalEnum(Enum):
    """"""

    FOO = generated.smoke_StandaloneExternalEnum.FOO

    @property
    def _native(self):
        return self.value

