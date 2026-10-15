

from smoke.OuterName import OuterName
from enum import Enum
import typing
from typing import Optional

class UseInnerName:

    def do_foo(self) -> OuterName.InnerName:
        ...
