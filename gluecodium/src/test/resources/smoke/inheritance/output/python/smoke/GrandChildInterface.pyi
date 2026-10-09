

from smoke.ChildInterface import ChildInterface
from enum import Enum
import typing
from typing import Optional

class GrandChildInterface(
    ChildInterface):

    def grand_child_method(self):
        ...
