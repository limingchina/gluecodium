

import typing

from enum import Enum

import generated


class QuxEnum(Enum):
    """"""

    QUX_ITEM = generated.smoke_QuxEnum.QUX_ITEM

    @property
    def _native(self):
        return self.value

