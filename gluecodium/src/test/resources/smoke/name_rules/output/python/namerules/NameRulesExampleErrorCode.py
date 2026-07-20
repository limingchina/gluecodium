

from __future__ import annotations


from enum import Enum

import generated


class NameRulesExampleErrorCode(Enum):
    """"""

    NONE = generated.NameRulesExampleErrorCode.NONE
    FATAL = generated.NameRulesExampleErrorCode.FATAL

    @property
    def _native(self):
        return self.value

