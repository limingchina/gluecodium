

from __future__ import annotations

from smoke.LambdasProducer import LambdasProducer

from typing import Callable

LambdasNullableConfuser = Callable[[Optional[str]], Optional[LambdasProducer]]

