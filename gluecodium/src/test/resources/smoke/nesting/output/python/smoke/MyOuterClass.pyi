

from smoke.MyParentInterface import MyParentInterface
from enum import Enum
import typing
from typing import Optional

class MyOuterClass:

    class MyNestedImplementation(
        MyParentInterface):
        ...
