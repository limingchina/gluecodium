

import typing

from enum import Enum

import generated


class ExternalEnum2(Enum):
    """"""

    ENABLED = generated.ExternalEnum2.ENABLED
    DISABLED = generated.ExternalEnum2.DISABLED

    @property
    def _native(self):
        return self.value

