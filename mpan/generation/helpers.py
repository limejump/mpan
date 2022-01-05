import random
import string

from ..distributor import Distributor
from ..mpan import MPAN
from ..profile_class import ProfileClass


def generate() -> str:

    profile_class = random.choice(tuple(ProfileClass.DESCRIPTIONS.keys()))

    mtc = random.randint(100, 999)

    llfc_options = string.ascii_uppercase + string.digits
    llfc = "".join([random.choice(llfc_options) for _ in range(3)])

    distributor = random.choice(
        tuple(Distributor.DNOS.keys()) + tuple(Distributor.IDNOS.keys())
    )
    identifier = random.randint(1000000000, 9999999999)

    pairs = zip(MPAN.PRIMES, f"{distributor}{identifier}")
    checksum = sum(prime * int(digit) for prime, digit in pairs) % 11 % 10

    return f"{profile_class}{mtc}{llfc}{distributor}{identifier}{checksum}"
