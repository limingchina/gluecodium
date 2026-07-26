

import typing

from enum import Enum

import generated


class ExposeInternalEnum(Enum):
    """"""

    FOO = generated.smoke_ExposeInternalEnum.FOO

    @property
    def _native(self):
        return self.value

