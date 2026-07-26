

import typing

from enum import Enum

import generated


class ExposeEnum(Enum):
    """"""

    FOO = generated.smoke_ExposeEnum.FOO

    @property
    def _native(self):
        return self.value

