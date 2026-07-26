

import typing

from enum import Enum

import generated


class EnumsSimpleEnum(Enum):
    """"""

    FIRST = generated.smoke_EnumsSimpleEnum.FIRST
    SECOND = generated.smoke_EnumsSimpleEnum.SECOND

    @property
    def _native(self):
        return self.value

