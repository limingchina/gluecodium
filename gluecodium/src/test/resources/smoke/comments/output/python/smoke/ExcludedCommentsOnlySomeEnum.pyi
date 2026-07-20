

import typing

from enum import Enum

import generated


class ExcludedCommentsOnlySomeEnum(Enum):
    """"""

    USELESS = generated.ExcludedCommentsOnlySomeEnum.USELESS

    @property
    def _native(self):
        return self.value

