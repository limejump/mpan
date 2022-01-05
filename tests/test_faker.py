from unittest import TestCase

from faker import Faker

from mpan import is_valid
from mpan.generation.faker import MPANProvider


class FakerTestCase(TestCase):
    def test_generation(self) -> None:
        fake = Faker()
        fake.add_provider(MPANProvider)
        self.assertTrue(is_valid(fake.mpan()))
