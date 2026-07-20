

from smoke.DateInterval import DateInterval
from smoke.Persistence import Persistence
from smoke.PseudoColor import PseudoColor
from smoke.SwiftSeason import SwiftSeason
import typing

from _native_base import _NativeBase

import generated


class UseSwiftExternalTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def date_interval_round_trip(input: DateInterval) -> DateInterval: ...

    @staticmethod
    def persistence_round_trip(input: Persistence) -> Persistence: ...

    @staticmethod
    def color_round_trip(input: PseudoColor) -> PseudoColor: ...

    @staticmethod
    def season_round_trip(input: SwiftSeason) -> SwiftSeason: ...

