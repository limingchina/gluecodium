

import typing

from enum import Enum

import generated


class EnumsExternal_Enum(Enum):
    """"""

    FOO_VALUE = generated.EnumsExternal_Enum.Foo_Value
    BAR_VALUE = generated.EnumsExternal_Enum.Bar_Value

    @property
    def _native(self):
        return self.value

