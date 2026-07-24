

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

import datetime
from smoke.FreeEnum import FreeEnum

from typing import Callable

FreeLambda = Callable[[datetime.datetime], FreeEnum]

