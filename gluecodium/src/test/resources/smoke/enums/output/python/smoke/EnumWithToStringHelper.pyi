

import typing

from enum import Enum

import generated


class EnumWithToStringHelper(Enum):
    """"""

    FIRST = generated.smoke_EnumWithToStringHelper.FIRST
    SECOND = generated.smoke_EnumWithToStringHelper.SECOND

    @property
    def _native(self):
        return self.value

