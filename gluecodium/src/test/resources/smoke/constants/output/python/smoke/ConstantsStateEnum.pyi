

import typing

from enum import Enum

import generated


class ConstantsStateEnum(Enum):
    """"""

    OFF = generated.smoke_ConstantsStateEnum.OFF
    ON = generated.smoke_ConstantsStateEnum.ON

    @property
    def _native(self):
        return self.value

