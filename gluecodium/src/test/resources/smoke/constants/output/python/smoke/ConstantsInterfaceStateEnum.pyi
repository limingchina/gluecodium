

import typing

from enum import Enum

import generated


class ConstantsInterfaceStateEnum(Enum):
    """"""

    OFF = generated.smoke_ConstantsInterfaceStateEnum.OFF
    ON = generated.smoke_ConstantsInterfaceStateEnum.ON

    @property
    def _native(self):
        return self.value

