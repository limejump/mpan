from typing import Optional

from .common import Subsection


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
