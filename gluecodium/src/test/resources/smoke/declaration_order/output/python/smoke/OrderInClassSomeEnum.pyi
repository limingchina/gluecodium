

import typing

from enum import Enum

import generated


class OrderInClassSomeEnum(Enum):
    """"""

    FOO = generated.OrderInClassSomeEnum.FOO
    BAR = generated.OrderInClassSomeEnum.BAR

    @property
    def _native(self):
        return self.value

