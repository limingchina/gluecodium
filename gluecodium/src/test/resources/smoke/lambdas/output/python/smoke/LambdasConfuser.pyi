

from smoke.LambdasProducer import LambdasProducer
import typing
from typing import Callable

#: Should confuse everyone thoroughly
LambdasConfuser = Callable[[str], Callable[[], str]]

