

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional
from typing import Callable

from smoke.LambdasInterface import LambdasInterface

LambdasWithStructuredTypesClassCallback = Callable[[LambdasInterface], None]

