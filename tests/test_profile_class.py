from unittest import TestCase

from mpan.profile_class import ProfileClass


class ProfileClassTestCase(TestCase):
    def setUp(self):
        self.pc = ProfileClass(identifier="04")

    def test_is_valid(self):
        self.assertTrue(self.pc)
        self.assertFalse(ProfileClass(identifier="test"))

    def test_description(self):
        self.assertEqual(self.pc.description, "Non-domestic Economy 7")
        self.assertEqual(ProfileClass("").description, None)
