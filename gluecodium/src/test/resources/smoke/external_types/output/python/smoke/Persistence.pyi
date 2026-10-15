

from enum import Enum
import typing
from typing import Optional

class Persistence(Enum):

    NONE = 0
    FOR_SESSION = 1
    PERMANENT = 2
