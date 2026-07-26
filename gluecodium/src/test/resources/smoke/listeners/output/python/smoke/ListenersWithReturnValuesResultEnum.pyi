

import typing

from enum import Enum

import generated


class ListenersWithReturnValuesResultEnum(Enum):
    """"""

    NONE = generated.smoke_ListenersWithReturnValuesResultEnum.NONE
    RESULT = generated.smoke_ListenersWithReturnValuesResultEnum.RESULT

    @property
    def _native(self):
        return self.value

