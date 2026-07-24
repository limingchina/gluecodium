

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.ClassInStructFooChecker import ClassInStructFooChecker

from typing import Callable

ClassInStructSomeLambda = Callable[[ClassInStructFooChecker], None]

