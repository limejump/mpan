from datetime import date
from typing import List

from .common import Subsection
from .data import GSP_IDS, ID_LOOKUP


class Distributor(Subsection):
    @property
    def is_dno(self) -> bool:
        try:
            return 0 < int(self.identifier) < 24
        except ValueError:
            return False

    @property
    def is_idno(self) -> bool:
        try:
            return 23 < int(self.identifier) < 39
        except ValueError:
            return False

    @property
    def name(self) -> str:
        return ID_LOOKUP[self.identifier]["name"]

    @property
    def participant_id(self) -> str:
        return ID_LOOKUP[self.identifier]["id"]

    @property
    def gsp_group_ids(self) -> List[str]:

        now = date.today()

        r = []
        for gsp_id, (started, stopped) in GSP_IDS[self.participant_id]:
            if now > started:
                if not stopped or stopped > now:
                    r.append(gsp_id)

        return r

    # Convenience properties

    @property
    def type(self) -> str:
        if self.is_dno:
            return "DNO"
        return "IDNO"

    @property
    def is_valid(self) -> bool:
        return self.is_dno or self.is_idno
