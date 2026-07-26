

import typing

from enum import Enum

import generated


class OrderInClassSomeEnum(Enum):
    """"""

    FOO = generated.smoke_OrderInClassSomeEnum.FOO
    BAR = generated.smoke_OrderInClassSomeEnum.BAR

    @property
    def _native(self):
        return self.value

