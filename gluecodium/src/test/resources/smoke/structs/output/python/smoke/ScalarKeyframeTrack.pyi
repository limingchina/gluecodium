

from smoke.ScalarKeyframe import ScalarKeyframe
from enum import Enum
import typing
from typing import Optional

class ScalarKeyframeTrack:

    keyframes: list[ScalarKeyframe]

    easing_function: str

    interpolation_mode: str
