

from __future__ import annotations


from enum import Enum

import generated


class ExternalEnum3(Enum):
    """"""

    ENABLED = generated.foo::AlienEnum3.ENABLED
    DISABLED = generated.foo::AlienEnum3.DISABLED

    @property
    def _native(self):
        return self.value

