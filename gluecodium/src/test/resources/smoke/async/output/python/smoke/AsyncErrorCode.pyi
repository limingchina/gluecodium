

import typing

from enum import Enum

import generated


class AsyncErrorCode(Enum):
    """"""

    VALUE1 = generated.smoke_AsyncErrorCode.VALUE1

    @property
    def _native(self):
        return self.value

