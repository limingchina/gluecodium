

import typing

from enum import Enum

import generated


class ExternalClasssome_Enum(Enum):
    """"""

    SOME_VALUE = generated.smoke_ExternalClasssome_Enum.SOME_VALUE

    @property
    def _native(self):
        return self.value

