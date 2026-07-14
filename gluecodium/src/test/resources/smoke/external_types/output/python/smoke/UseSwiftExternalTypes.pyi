

from smoke.DateInterval import DateInterval
from smoke.Persistence import Persistence
from smoke.PseudoColor import PseudoColor
from smoke.SwiftSeason import SwiftSeason


from _native_base import _NativeBase

import generated


class UseSwiftExternalTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def date_interval_round_trip(input: DateInterval) -> DateInterval:
        """"""
        native_result = generated.UseSwiftExternalTypes.date_interval_round_trip(input._native)
        return DateInterval(native_result)

    @staticmethod
    def persistence_round_trip(input: Persistence) -> Persistence:
        """"""
        native_result = generated.UseSwiftExternalTypes.persistence_round_trip(input._native)
        return Persistence(native_result)

    @staticmethod
    def color_round_trip(input: PseudoColor) -> PseudoColor:
        """"""
        native_result = generated.UseSwiftExternalTypes.color_round_trip(input._native)
        return PseudoColor(native_result)

    @staticmethod
    def season_round_trip(input: SwiftSeason) -> SwiftSeason:
        """"""
        native_result = generated.UseSwiftExternalTypes.season_round_trip(input._native)
        return SwiftSeason(native_result)

