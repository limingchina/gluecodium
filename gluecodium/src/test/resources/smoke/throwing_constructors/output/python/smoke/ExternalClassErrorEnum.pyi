

import typing

from enum import Enum

import generated


class ExternalClassErrorEnum(Enum):
    """"""

    NONE = generated.smoke_ExternalClassErrorEnum.NONE
    CRASHED = generated.smoke_ExternalClassErrorEnum.CRASHED

    @property
    def _native(self):
        return self.value

