

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.Persistence import Persistence
from smoke.PseudoColor import PseudoColor

dict[Persistence, PseudoColor] = dict[Persistence, PseudoColor]

