

import typing

from enum import Enum

import generated


class ExcludedCommentsOnlySomeEnum(Enum):
    """"""

    USELESS = generated.smoke_ExcludedCommentsOnlySomeEnum.USELESS

    @property
    def _native(self):
        return self.value

