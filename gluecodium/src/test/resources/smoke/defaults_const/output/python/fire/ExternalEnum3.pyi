

import typing

from enum import Enum

import generated


class ExternalEnum3(Enum):
    """"""

    ENABLED = generated.fire_ExternalEnum3.ENABLED
    DISABLED = generated.fire_ExternalEnum3.DISABLED

    @property
    def _native(self):
        return self.value

