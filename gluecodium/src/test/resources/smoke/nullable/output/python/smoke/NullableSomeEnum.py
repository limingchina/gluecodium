

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class NullableSomeEnum(Enum):

    ON = generated.smoke_NullableSomeEnum.ON
    OFF = generated.smoke_NullableSomeEnum.OFF

    @property
    def _native(self):
        return self.value

