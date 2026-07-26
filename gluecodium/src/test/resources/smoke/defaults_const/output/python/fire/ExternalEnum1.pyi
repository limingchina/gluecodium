

import typing

from enum import Enum

import generated


class ExternalEnum1(Enum):
    """"""

    ENABLED = generated.fire_ExternalEnum1.ENABLED
    DISABLED = generated.fire_ExternalEnum1.DISABLED

    @property
    def _native(self):
        return self.value

