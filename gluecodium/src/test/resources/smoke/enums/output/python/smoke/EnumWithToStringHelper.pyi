

import typing

from enum import Enum

import generated


class EnumWithToStringHelper(Enum):
    """"""

    FIRST = generated.EnumWithToStringHelper.FIRST
    SECOND = generated.EnumWithToStringHelper.SECOND

    @property
    def _native(self):
        return self.value

