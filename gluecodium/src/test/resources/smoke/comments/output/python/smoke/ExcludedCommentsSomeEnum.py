

from __future__ import annotations


from enum import Enum

import generated


class ExcludedCommentsSomeEnum(Enum):
    """This is some very useful enum."""

    USELESS = generated.ExcludedCommentsSomeEnum.USELESS

    @property
    def _native(self):
        return self.value

