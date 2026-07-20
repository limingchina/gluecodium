

import typing

from enum import Enum

import generated


class CppRefReturnTypeInternalError(Enum):
    """"""

    FOO = generated.CppRefReturnTypeInternalError.FOO
    BAR = generated.CppRefReturnTypeInternalError.BAR

    @property
    def _native(self):
        return self.value

