

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional
from typing import Callable

from smoke.ClassInStructFooChecker import ClassInStructFooChecker

ClassInStructSomeLambda = Callable[[ClassInStructFooChecker], None]

