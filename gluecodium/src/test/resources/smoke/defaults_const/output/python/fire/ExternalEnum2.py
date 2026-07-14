

from __future__ import annotations


from enum import Enum

import generated


class ExternalEnum2(Enum):
    """"""

    ENABLED = generated.foo::AlienEnum2.ENABLED
    DISABLED = generated.foo::AlienEnum2.DISABLED

    @property
    def _native(self):
        return self.value

