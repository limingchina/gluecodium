

from enum import Enum
import typing
from typing import Optional

class ListenerInterface:

    def notify(self):
        ...
