

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.LambdasInterface import LambdasInterface

from typing import Callable

LambdasWithStructuredTypesClassCallback = Callable[[LambdasInterface], None]

