

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.InterfaceInInterfaceFooChecker import InterfaceInInterfaceFooChecker

from typing import Callable

InterfaceInInterfaceSomeLambda = Callable[[InterfaceInInterfaceFooChecker], None]

