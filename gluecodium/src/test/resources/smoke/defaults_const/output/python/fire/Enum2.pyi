

import typing

from enum import Enum

import generated


class Enum2(Enum):
    """"""

    ENABLED = generated.fire_Enum2.ENABLED
    DISABLED = generated.fire_Enum2.DISABLED

    @property
    def _native(self):
        return self.value

