

import typing

from enum import Enum

import generated


class ListenerWithPropertiesResultEnum(Enum):
    """"""

    NONE = generated.smoke_ListenerWithPropertiesResultEnum.NONE
    RESULT = generated.smoke_ListenerWithPropertiesResultEnum.RESULT

    @property
    def _native(self):
        return self.value

