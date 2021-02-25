#
# Reference:
#   https://en.wikipedia.org/wiki/Meter_Point_Administration_Number
#   https://en.wikipedia.org/wiki/Distribution_network_operator
#

import re

from dataclasses import dataclass
from typing import Optional


class InvalidMPANError(Exception):
    pass


class Subsection:
    """
    A string-like object that includes additional information we know based on
    the identifier.
    """

    def __init__(self, identifier: str) -> None:
        self.identifier = identifier

    def __str__(self) -> str:
        return self.identifier

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}: {self.identifier}"

    def __bool__(self) -> bool:
        return self.is_valid

    @property
    def is_valid(self) -> bool:
        raise NotImplementedError()


class Distributor(Subsection):

    DNOS = {
        "10": {
            "area": "Eastern England",
            "operator": "UK Power Networks",
            "participant_id": "EELC",
            "gsp_group_id": "_A",
        },
        "11": {
            "area": "East Midlands",
            "operator": "Western Power Distribution",
            "participant_id": "EMEB",
            "gsp_group_id": "_B",
        },
        "12": {
            "area": "London",
            "operator": "UK Power Networks",
            "participant_id": "LOND",
            "gsp_group_id": "_C",
        },
        "13": {
            "area": "Merseyside and Northern Wales",
            "operator": "SP Energy Networks",
            "participant_id": "MANW",
            "gsp_group_id": "_D",
        },
        "14": {
            "area": "West Midlands",
            "operator": "Western Power Distribution",
            "participant_id": "MIDE",
            "gsp_group_id": "_E",
        },
        "15": {
            "area": "North Eastern England",
            "operator": "Northern Powergrid",
            "participant_id": "NEEB",
            "gsp_group_id": "_F",
        },
        "16": {
            "area": "North Western England",
            "operator": "Electricity North West",
            "participant_id": "NORW",
            "gsp_group_id": "_G",
        },
        "17": {
            "area": "Northern Scotland",
            "operator": "Scottish & Southern Electricity Networks",
            "participant_id": "HYDE",
            "gsp_group_id": "_P",
        },
        "18": {
            "area": "Southern Scotland",
            "operator": "SP Energy Networks, 0330 10 10 444",
            "participant_id": "SPOW",
            "gsp_group_id": "_N",
        },
        "19": {
            "area": "South Eastern England",
            "operator": "UK Power Networks",
            "participant_id": "SEEB",
            "gsp_group_id": "_J",
        },
        "20": {
            "area": "Southern England",
            "operator": "Scottish & Southern Electricity Networks",
            "participant_id": "SOUT",
            "gsp_group_id": "_H",
        },
        "21": {
            "area": "Southern Wales",
            "operator": "Western Power Distribution",
            "participant_id": "SWAE",
            "gsp_group_id": "_K",
        },
        "22": {
            "area": "South Western England",
            "operator": "Western Power Distribution",
            "participant_id": "SWEB",
            "gsp_group_id": "_L",
        },
        "23": {
            "area": "Yorkshire",
            "operator": "Northern Powergrid",
            "participant_id": "YELG",
            "gsp_group_id": "_M",
        },
    }

    IDNOS = {
        "24": {
            "name": "Envoy",
            "licensee": "Independent Power Networks",
            "mpas_operator_id": "IPNL",
        },
        "25": {
            "name": "ESP Electricity",
            "licensee": "ESP Electricity",
            "mpas_operator_id": "LENG",
        },
        "26": {
            "name": "Last Mile Electricity",
            "licensee": "Last Mile Electricity",
            "mpas_operator_id": "GUCL",
        },
        "27": {
            "name": "GTC",
            "licensee": "The Electricity Network Company Ltd",
            "mpas_operator_id": "ETCL",
        },
        "28": {
            "name": "EDF IDNO",
            "licensee": "UK Power Networks (IDNO) Ltd",
            "mpas_operator_id": "EDFI",
        },
        "29": {
            "name": "Harlaxton Energy Networks Ltd",
            "licensee": "Harlaxton (IDNO)",
            "mpas_operator_id": "HARL",
        },
        "30": {
            "name": "Leep Electricity Networks Ltd",
            "licensee": "Leep Electricity Networks (IDNO)",
            "mpas_operator_id": "PENL",
        },
        "31": {
            "name": "UK Power Distribution Ltd",
            "licensee": "UK Power Distribution Ltd",
            "mpas_operator_id": "UKPD",
        },
        "32": {
            "name": "Energy Assets Networks Ltd",
            "licensee": "Energy Assets Networks Ltd.",
            "mpas_operator_id": "UDNL",
        },
        "33": {
            "name": "Eclipse Power Networks",
            "licensee": "Eclipse Power Networks",
            "mpas_operator_id": "GGEN",
        },
        "34": {
            "name": "Murphy Power",
            "licensee": "Murphy Power",
            "mpas_operator_id": "MPDL",
        },
        "35": {
            "name": "Fulcrum Electricity Assets",
            "licensee": "Fulcrum Electricity Assets",
            "mpas_operator_id": "FEAL",
        },
        "36": {
            "name": "Vattenfall Networks Ltd",
            "licensee": "Vattenfall Networks Ltd",
            "mpas_operator_id": "VATT",
        },
    }

    @property
    def is_valid(self) -> bool:
        return self.is_dno or self.is_idno

    @property
    def area(self) -> str:
        return self._from_definitions(self.DNOS, "area")

    @property
    def operator(self) -> str:
        return self._from_definitions(self.DNOS, "operator")

    @property
    def participant_id(self) -> str:
        return self._from_definitions(self.DNOS, "participant_id")

    @property
    def gsp_group_id(self) -> str:
        return self._from_definitions(self.DNOS, "gsp_group_id")

    @property
    def name(self) -> str:
        return self._from_definitions(self.IDNOS, "name")

    @property
    def licensee(self) -> str:
        return self._from_definitions(self.IDNOS, "licensee")

    @property
    def mpas_operator_id(self) -> str:
        return self._from_definitions(self.IDNOS, "mpas_operator_id")

    @property
    def is_dno(self) -> bool:
        return self.identifier in self.DNOS

    @property
    def is_idno(self) -> bool:
        return self.identifier in self.IDNOS

    def _from_definitions(self, source: dict, key: str) -> Optional[str]:
        try:
            return source[self.identifier][key]
        except KeyError:
            return None


class ProfileClass(Subsection):

    DESCRIPTIONS = {
        "00": "Half-hourly supply (import and export)",
        "01": "Domestic unrestricted",
        "02": "Domestic Economy meter of two or more rates",
        "03": "Non-domestic unrestricted",
        "04": "Non-domestic Economy 7",
        "05": (
            "Non-domestic, with maximum demand (MD) recording capability and "
            "with load factor (LF) less than or equal to 20%"
        ),
        "06": (
            "Non-domestic, with MD recording capability and with LF less than "
            "or equal to 30% and greater than 20%"
        ),
        "07": (
            "Non-domestic, with MD recording capability and with LF less than "
            "or equal to 40% and greater than 30%"
        ),
        "08": (
            "Non-domestic, with MD recording capability and with LF greater "
            "than 40% (also all non-half-hourly export MSIDs)"
        ),
    }

    @property
    def is_valid(self) -> bool:
        return self.identifier in self.DESCRIPTIONS

    @property
    def description(self) -> Optional[str]:
        try:
            return self.DESCRIPTIONS[self.identifier]
        except KeyError:
            return None


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

        raise InvalidMPANError("This doesn't look like an MPAN")

    def __str__(self) -> str:
        return self._raw

    def __repr__(self):
        return str(self)

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


def is_valid(raw_string: str) -> bool:
    try:
        return MPAN(raw_string).is_valid
    except InvalidMPANError:
        return False
