

import typing

from enum import Enum

import generated


class ErrorsInterfaceExternalErrors(Enum):
    """"""

    NONE = generated.ErrorsInterfaceExternalErrors.NONE
    BOOM = generated.ErrorsInterfaceExternalErrors.BOOM
    BUST = generated.ErrorsInterfaceExternalErrors.BUST

    @property
    def _native(self):
        return self.value

