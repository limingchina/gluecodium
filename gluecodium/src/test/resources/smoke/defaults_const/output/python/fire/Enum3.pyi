

import typing

from enum import Enum

import generated


class Enum3(Enum):
    """"""

    ENABLED = generated.fire_Enum3.ENABLED
    DISABLED = generated.fire_Enum3.DISABLED

    @property
    def _native(self):
        return self.value

