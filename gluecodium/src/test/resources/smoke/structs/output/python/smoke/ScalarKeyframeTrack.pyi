

from smoke.ScalarKeyframe import ScalarKeyframe
from enum import Enum
import typing
from typing import Optional

class ScalarKeyframeTrack:
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, keyframes: list[ScalarKeyframe], easing_function: str, interpolation_mode: str) -> None: ...

    keyframes: list[ScalarKeyframe]

    easing_function: str

    interpolation_mode: str
