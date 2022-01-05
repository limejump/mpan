from .exceptions import InvalidMPANError
from .mpan import MPAN


def is_valid(raw_string: str) -> bool:
    try:
        return MPAN(raw_string).is_valid
    except InvalidMPANError:
        return False
