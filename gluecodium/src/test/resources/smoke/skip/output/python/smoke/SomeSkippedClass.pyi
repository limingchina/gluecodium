

from dont.smoke.DontSmokeEnum import DontSmokeEnum
from enum import Enum
import typing

class SomeSkippedClass:

    def do_foo(self) -> DontSmokeEnum:
        ...


