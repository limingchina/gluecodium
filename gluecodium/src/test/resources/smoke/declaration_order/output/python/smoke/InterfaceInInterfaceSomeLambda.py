

from __future__ import annotations

from smoke.InterfaceInInterfaceFooChecker import InterfaceInInterfaceFooChecker

from typing import Callable

InterfaceInInterfaceSomeLambda = Callable[[InterfaceInInterfaceFooChecker], None]

