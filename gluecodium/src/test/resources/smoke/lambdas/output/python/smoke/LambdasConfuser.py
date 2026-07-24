

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.LambdasProducer import LambdasProducer

from typing import Callable

LambdasConfuser = Callable[[str], LambdasProducer]

