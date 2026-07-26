

import typing

from enum import Enum

import generated


class Persistence(Enum):
    """"""

    NONE = generated.smoke_Persistence.NONE
    FOR_SESSION = generated.smoke_Persistence.FOR_SESSION
    PERMANENT = generated.smoke_Persistence.PERMANENT

    @property
    def _native(self):
        return self.value

