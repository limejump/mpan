from unittest import TestCase

from mpan.helpers import is_valid

from .common import INVALID, UNPARSEABLE, VALID


class IsValidTestCase(TestCase):
    def test_is_valid(self):
        for string in VALID:
            with self.subTest(string=string):
                self.assertTrue(is_valid(string), string)

    def test_is_valid_fail(self):
        for string in INVALID:
            with self.subTest(string=string):
                self.assertFalse(is_valid(string))
        for string in UNPARSEABLE:
            with self.subTest(string=string):
                self.assertFalse(is_valid(string))
