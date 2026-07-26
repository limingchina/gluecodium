

import typing

from enum import Enum

import generated


class EnumsInTypeCollectionTCEnum(Enum):
    """"""

    FIRST = generated.smoke_EnumsInTypeCollectionTCEnum.FIRST
    SECOND = generated.smoke_EnumsInTypeCollectionTCEnum.SECOND

    @property
    def _native(self):
        return self.value

