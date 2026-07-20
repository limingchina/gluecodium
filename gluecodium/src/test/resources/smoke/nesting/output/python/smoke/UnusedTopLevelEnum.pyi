

import typing

from enum import Enum

import generated


class UnusedTopLevelEnum(Enum):
    """"""

    DOESNT_WORK = generated.UnusedTopLevelEnum.DOESNT_WORK
    CRASHED_ANYWAY = generated.UnusedTopLevelEnum.CRASHED_ANYWAY

    @property
    def _native(self):
        return self.value

