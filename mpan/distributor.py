from typing import Optional

from .common import Subsection


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
