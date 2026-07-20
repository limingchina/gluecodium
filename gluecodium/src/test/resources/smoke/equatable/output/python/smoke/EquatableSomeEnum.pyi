

import typing

from enum import Enum

import generated


class EquatableSomeEnum(Enum):
    """"""

    FOO = generated.EquatableSomeEnum.FOO
    BAR = generated.EquatableSomeEnum.BAR

    @property
    def _native(self):
        return self.value

