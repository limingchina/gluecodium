

from smoke.ParentInterface import ParentInterface
from enum import Enum
import typing
from typing import Optional

class ChildClassFromInterface(
    ParentInterface):

    def child_class_method(self):
        ...
