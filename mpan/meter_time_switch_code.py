from dataclasses import dataclass
from typing import Optional

from .common import Subsection


class MeterTimeSwitchCode(Subsection):
    @dataclass
    class MTCRange:
        upper: int
        lower: int
        description: str

    MTC_RANGES = (
        MTCRange(1, 399, "DNO specific"),
        MTCRange(400, 499, "Reserved"),
        MTCRange(
            500,
            509,
            "Codes for related Metering Systems – common across the Industry",
        ),
        MTCRange(
            510, 799, "Codes for related Metering Systems – DNO specific"
        ),
        MTCRange(800, 999, "Codes common across the Industry"),
    )

    @property
    def is_valid(self) -> bool:
        try:
            return 0 < int(self.identifier) < 1000
        except ValueError:
            return False

    @property
    def description(self) -> Optional[str]:

        if not self.identifier:
            return None

        try:
            value = int(self.identifier)
        except ValueError:
            return None

        for range_ in self.MTC_RANGES:
            if range_.upper <= value <= range_.lower:
                return range_.description

        return None
