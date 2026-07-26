

import typing

from enum import Enum

import generated


class EnumStartsWithOne(Enum):
    """"""

    FIRST = generated.smoke_EnumStartsWithOne.FIRST
    SECOND = generated.smoke_EnumStartsWithOne.SECOND

    @property
    def _native(self):
        return self.value

