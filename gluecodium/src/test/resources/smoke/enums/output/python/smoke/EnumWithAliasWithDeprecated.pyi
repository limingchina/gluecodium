

import typing

from enum import Enum

import generated


class EnumWithAliasWithDeprecated(Enum):
    """"""

    ONE = generated.EnumWithAliasWithDeprecated.ONE
    TWO = generated.EnumWithAliasWithDeprecated.TWO
    THREE = generated.EnumWithAliasWithDeprecated.THREE
    FIRST = generated.EnumWithAliasWithDeprecated.FIRST

    @property
    def _native(self):
        return self.value

