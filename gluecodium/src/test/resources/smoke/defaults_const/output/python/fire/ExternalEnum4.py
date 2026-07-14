

from __future__ import annotations


from enum import Enum

import generated


class ExternalEnum4(Enum):
    """"""

    ENABLED = generated.foo::AlienEnum4.ENABLED
    DISABLED = generated.foo::AlienEnum4.DISABLED

    @property
    def _native(self):
        return self.value

