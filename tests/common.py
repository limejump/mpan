import json

from pathlib import Path


# These can't be handled at all by the library
UNPARSEABLE = (
    "Not an MPAN",
    "42",
)

# These look legit, but don't pass the validation
INVALID = (
    "2499999999990",  # Bad checksum
    "8699999999991",  # Bad distributor
    "991112221312345678907",  # Bad profile class
    "000002221312345678907",  # Bad mtc
)


def get_valid_mpans() -> list:
    """
    For privacy reasons, valid MPANs cannot be included in this project
    directly.  Instead, if you want to test for a list of MPANs you know to be
    legitimate, you must provide them yourself in a file called
    `tests/data/valid-mpans.json`.  This file should be a JSON list of strings
    and/or integers, like this:

      [
        "1234567890123456789012",
        "1234567890123",
        1234567890123456789012,
        1234567890123
      ]

    """
    path = Path(__file__).parent / "data" / "valid-mpans.json"
    if not path.exists():
        return []
    with path.open() as f:
        return json.load(f)
