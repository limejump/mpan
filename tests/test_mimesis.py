from unittest import TestCase

from mimesis import Generic
from mimesis.locales import Locale

from mpan import is_valid
from mpan.generation.mimesis import MPANProvider


class FakerTestCase(TestCase):
    def test_generation(self) -> None:
        generic = Generic(locale=Locale.DEFAULT)
        generic.add_provider(MPANProvider)
        self.assertTrue(is_valid(generic.mpan.generate()))
