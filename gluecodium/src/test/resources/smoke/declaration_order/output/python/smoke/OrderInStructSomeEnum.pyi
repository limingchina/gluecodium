

import typing

from enum import Enum

import generated


class OrderInStructSomeEnum(Enum):
    """"""

    FOO = generated.smoke_OrderInStructSomeEnum.FOO
    BAR = generated.smoke_OrderInStructSomeEnum.BAR

    @property
    def _native(self):
        return self.value

