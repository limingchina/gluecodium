

from dont.smoke.DontSmokeEnum import DontSmokeEnum
from enum import Enum
import typing
from typing import Optional

class SomeSkippedClass:

    def do_foo(self) -> DontSmokeEnum:
        ...
