

import typing

from enum import Enum

import generated


class ErrorsExternalErrors(Enum):
    """"""

    NONE = generated.smoke_ErrorsExternalErrors.NONE
    BOOM = generated.smoke_ErrorsExternalErrors.BOOM
    BUST = generated.smoke_ErrorsExternalErrors.BUST

    @property
    def _native(self):
        return self.value

