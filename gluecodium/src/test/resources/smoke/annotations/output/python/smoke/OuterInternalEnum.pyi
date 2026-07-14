


from enum import Enum

import generated


class OuterInternalEnum(Enum):
    """"""

    FIRST = generated.OuterInternalEnum.FIRST
    SECOND = generated.OuterInternalEnum.SECOND

    @property
    def _native(self):
        return self.value

