

import typing

from enum import Enum

import generated


class DeprecationCommentsOnlySomeEnum(Enum):
    """"""

    USELESS = generated.smoke_DeprecationCommentsOnlySomeEnum.USELESS

    @property
    def _native(self):
        return self.value

