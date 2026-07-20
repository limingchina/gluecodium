

import typing

from enum import Enum

import generated


class EnumsInTypeCollectionTCEnum(Enum):
    """"""

    FIRST = generated.EnumsInTypeCollectionTCEnum.FIRST
    SECOND = generated.EnumsInTypeCollectionTCEnum.SECOND

    @property
    def _native(self):
        return self.value

