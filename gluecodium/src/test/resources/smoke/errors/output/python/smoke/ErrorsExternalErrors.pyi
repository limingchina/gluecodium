

import typing

from enum import Enum

import generated


class ErrorsExternalErrors(Enum):
    """"""

    NONE = generated.ErrorsExternalErrors.NONE
    BOOM = generated.ErrorsExternalErrors.BOOM
    BUST = generated.ErrorsExternalErrors.BUST

    @property
    def _native(self):
        return self.value

