

import typing

from enum import Enum

import generated


class OuterInternalEnum(Enum):
    """"""

    FIRST = generated.smoke_OuterInternalEnum.FIRST
    SECOND = generated.smoke_OuterInternalEnum.SECOND

    @property
    def _native(self):
        return self.value

