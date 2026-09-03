

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.Persistence import Persistence
from smoke.PseudoColor import PseudoColor

ExternalMap = dict[Persistence, PseudoColor]


