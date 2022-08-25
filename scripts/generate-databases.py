#!/usr/bin/env python3

import csv
import sys

from argparse import ArgumentParser, ArgumentTypeError
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from subprocess import run


class Command:
    """
    To make updating the internal database easier and less error-prone, we use
    this script to generate `mpan/data.py` based on an industry CSV.
    """

    TARGET = (Path(__file__).parent / ".." / "mpan" / "data.py").absolute()

    #
    # These values are all scraped from Wikipedia:
    # https://en.wikipedia.org/wiki/Distribution_network_operator
    # https://en.wikipedia.org/wiki/Meter_Point_Administration_Number
    #
    # As well as from Ofgem:
    # https://www.ofgem.gov.uk/sites/default/files/2022-07/Copy%20of%20Electricity%20Registered%20or%20service%20addresses%20NEW%201.0.pdf
    #
    ID_LOOKUP = {
        "10": {"id": "EELC", "name": "UK Power Networks"},
        "11": {"id": "EMEB", "name": "Western Power Distribution"},
        "12": {"id": "LOND", "name": "UK Power Networks"},
        "13": {"id": "MANW", "name": "SP Energy Networks"},
        "14": {"id": "MIDE", "name": "Western Power Distribution"},
        "15": {"id": "NEEB", "name": "Northern Powergrid (Northeast)"},
        "16": {"id": "NORW", "name": "Electricity North West"},
        "17": {"id": "HYDE", "name": "SSE (Scottish Hydro Electric)"},
        "18": {"id": "SPOW", "name": "SP Energy Networks"},
        "19": {"id": "SEEB", "name": "UK Power Networks"},
        "20": {"id": "SOUT", "name": "SSE (Southern Electric)"},
        "21": {"id": "SWAE", "name": "Western Power Distribution"},
        "22": {"id": "SWEB", "name": "Western Power Distribution"},
        "23": {"id": "YELG", "name": "Northern Powergrid (Yorkshire)"},
        "24": {"id": "IPNL", "name": "Independent Power Networks Ltd."},
        "25": {"id": "LENG", "name": "ESP Electricity"},
        "26": {"id": "GUCL", "name": "Last Mile Electricity"},
        "27": {"id": "ETCL", "name": "The Electricity Network Company Ltd."},
        "28": {"id": "EDFI", "name": "UK Power Networks"},
        "29": {"id": "HARL", "name": "Harlaxton Energy Networks Ltd."},
        "30": {"id": "PENL", "name": "Leep Electricity Networks Ltd."},
        "31": {"id": "UKPD", "name": "UK Power Distribution Ltd."},
        "32": {"id": "UDNL", "name": "Energy Assets Networks Ltd."},
        "33": {"id": "GGEN", "name": "Eclipse Power Networks"},
        "34": {"id": "MPDL", "name": "Murphy Group"},
        "35": {"id": "FEAL", "name": "Fulcrum Electricity Assets"},
        "36": {"id": "VATT", "name": "Vattenfall Networks Ltd."},
        "37": {"id": "FORB", "name": "Optimal Power Networks Ltd."},
        "38": {"id": "INDI", "name": "Indigo Power Limited"},
    }

    def __init__(self) -> None:

        self.parser = ArgumentParser(
            description=(
                "The local database of MPAN-related data has to be updated "
                "from time to time.  We use this script to do that."
            )
        )
        self.parser.add_argument(
            "source",
            type=self._ensure_is_file,
            help=(
                "The path to the local copy of your "
                "GSP_Group_Distributor_nnn.csv file."
            ),
        )
        self.args = self.parser.parse_args()

    def __call__(self, *args, **kwargs) -> int:

        with self.args.source.open() as f:

            reader = csv.reader(f)
            next(reader)  # Skip the header

            db = defaultdict(list)
            for row in reader:

                gsp_id = row[0]
                started = datetime.strptime(row[4], "%d/%m/%Y").date()
                stopped = None
                if row[5]:
                    stopped = datetime.strptime(row[5], "%d/%m/%Y").date()

                db[row[1]].append((gsp_id, (started, stopped)))

        with self.TARGET.open("w") as f:
            f.write("import datetime\n\n\n")
            f.write("ID_LOOKUP = " + repr(self.ID_LOOKUP) + "\n\n")
            f.write("GSP_IDS = " + repr(dict(db)))

        run(("black", "--quiet", self.TARGET))

        return 0

    @staticmethod
    def _ensure_is_file(path: str) -> Path:

        path = Path(path)

        if not path.exists():
            raise ArgumentTypeError(f"The file {path} doesn't exist.")

        return path


if __name__ == "__main__":
    sys.exit(Command()())
