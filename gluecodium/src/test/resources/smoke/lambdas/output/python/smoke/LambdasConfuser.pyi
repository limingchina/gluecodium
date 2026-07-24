

from smoke.LambdasProducer import LambdasProducer
import typing
from typing import Callable

LambdasConfuser = Callable[[str], Callable[[], str]]

