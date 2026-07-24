

from smoke.LambdasProducer import LambdasProducer
import typing
from typing import Callable

LambdasNullableConfuser = Callable[[Optional[str]], Optional[Callable[[], str]]]

