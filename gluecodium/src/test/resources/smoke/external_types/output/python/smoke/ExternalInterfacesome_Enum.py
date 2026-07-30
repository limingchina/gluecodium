

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class ExternalInterfacesome_Enum(Enum):

    SOME_VALUE = generated.smoke_ExternalInterfacesome_Enum.SOME_VALUE

    @property
    def _native(self):
        return self.value

