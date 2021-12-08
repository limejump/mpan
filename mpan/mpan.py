#
# Reference:
#   https://en.wikipedia.org/wiki/Meter_Point_Administration_Number
#   https://en.wikipedia.org/wiki/Distribution_network_operator
#

import re

from typing import Optional

from .distributor import Distributor
from .exceptions import InvalidMPANError
from .meter_time_switch_code import MeterTimeSwitchCode
from .profile_class import ProfileClass


class MPAN:

    RE_SHORT = re.compile(r"^((\d\d)(\d{8})\d\d(\d))$")
    RE_LONG = re.compile(
        r"^((\d\d)(\d\d\d)([A-Z0-9]{3}))((\d\d)(\d{8})\d\d(\d))$"
    )

    # 11 is deliberately missing as-per the rules for the validation algorithm.
    PRIMES = [3, 5, 7, 13, 17, 19, 23, 29, 31, 37, 41, 43]

    def __init__(self, raw_string: str) -> None:

        self.top_line = None
        self.profile_class = None
        self.meter_time_switch_code = None
        self.line_loss_factor_class = None
        self.core = None
        self.distributor = None
        self.identifier = None
        self.checksum = None

        # To allow for objects that can be cast as strings
        self._raw = str(raw_string)

        if m := self.RE_SHORT.match(self._raw):
            self._parse_short(m)
            return

        if m := self.RE_LONG.match(self._raw):
            self._parse_long(m)
            return

        raise InvalidMPANError(f"{self._raw} doesn't look like an MPAN")

    def __str__(self) -> str:
        return self._raw

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, MPAN):
            return False
        return str(self) == str(other)

    @property
    def is_short(self) -> bool:
        return self.profile_class is None

    @property
    def is_long(self) -> bool:
        return not self.is_short

    @property
    def pc(self) -> Optional[ProfileClass]:
        return self.profile_class

    @property
    def mtc(self) -> Optional[MeterTimeSwitchCode]:
        return self.meter_time_switch_code

    @property
    def llfc(self) -> Optional[str]:
        return self.line_loss_factor_class

    @property
    def as_short(self) -> str:
        return self.core

    @property
    def is_valid(self) -> bool:
        """
        If this is a long MPAN, attempt to validate the top line and
        distributor by checking that those values conform to expected ranges.
        If that all looks good, perform the checksum for the bottom line.
        """

        if self.profile_class is not None:
            if not self.profile_class.is_valid:
                return False

        if self.meter_time_switch_code is not None:
            if not self.meter_time_switch_code.is_valid:
                return False

        if not self.distributor.is_valid:
            return False

        pairs = zip(self.PRIMES, self.core[:-1])
        result = sum(prime * int(digit) for prime, digit in pairs) % 11 % 10
        return result == int(self.checksum)

    def check(self) -> None:
        if not self.is_valid:
            raise InvalidMPANError(f"MPAN failed validity check: {self}")

    def _parse_short(self, m: re.Match) -> None:
        self.core = m.group(1)
        self.distributor = Distributor(m.group(2))
        self.identifier = m.group(3)
        self.checksum = m.group(4)

    def _parse_long(self, m: re.Match) -> None:

        self.top_line = m.group(1)
        self.profile_class = ProfileClass(m.group(2))
        self.meter_time_switch_code = MeterTimeSwitchCode(m.group(3))
        self.line_loss_factor_class = m.group(4)

        self.core = m.group(5)
        self.distributor = Distributor(m.group(6))
        self.identifier = m.group(7)
        self.checksum = m.group(8)
