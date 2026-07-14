


from enum import Enum

import generated


class StandaloneExternalEnum(Enum):
    """"""

    FOO = generated.StandaloneExternalEnum.foo

    @property
    def _native(self):
        return self.value

