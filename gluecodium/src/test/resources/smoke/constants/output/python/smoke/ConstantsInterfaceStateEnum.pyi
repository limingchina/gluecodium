

import typing

from enum import Enum

import generated


class ConstantsInterfaceStateEnum(Enum):
    """"""

    OFF = generated.ConstantsInterfaceStateEnum.OFF
    ON = generated.ConstantsInterfaceStateEnum.ON

    @property
    def _native(self):
        return self.value

