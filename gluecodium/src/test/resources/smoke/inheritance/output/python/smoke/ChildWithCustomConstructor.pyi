

from smoke.ParentWithCustomConstructor import ParentWithCustomConstructor
from enum import Enum
import typing
from typing import Optional

class ChildWithCustomConstructor(
    ParentWithCustomConstructor):

    @staticmethod
    def make() -> ChildWithCustomConstructor:
        ...
