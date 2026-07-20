

from __future__ import annotations


from enum import Enum

import generated


class commentsSomeEnum(Enum):
    """This is some very useful enum."""

    USELESS = generated.commentsSomeEnum.USELESS
    USEFUL = generated.commentsSomeEnum.USEFUL

    @property
    def _native(self):
        return self.value

