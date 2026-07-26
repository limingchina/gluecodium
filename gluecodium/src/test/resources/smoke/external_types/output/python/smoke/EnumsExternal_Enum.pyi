

import typing

from enum import Enum

import generated


class EnumsExternal_Enum(Enum):
    """"""

    FOO_VALUE = generated.smoke_EnumsExternal_Enum.FOO_VALUE
    BAR_VALUE = generated.smoke_EnumsExternal_Enum.BAR_VALUE

    @property
    def _native(self):
        return self.value

