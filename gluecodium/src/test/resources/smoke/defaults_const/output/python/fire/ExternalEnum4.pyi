

import typing

from enum import Enum

import generated


class ExternalEnum4(Enum):
    """"""

    ENABLED = generated.ExternalEnum4.ENABLED
    DISABLED = generated.ExternalEnum4.DISABLED

    @property
    def _native(self):
        return self.value

