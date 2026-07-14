

from __future__ import annotations


from enum import Enum

import generated


class ExternalEnum1(Enum):
    """"""

    ENABLED = generated.foo::AlienEnum1.ENABLED
    DISABLED = generated.foo::AlienEnum1.DISABLED

    @property
    def _native(self):
        return self.value

