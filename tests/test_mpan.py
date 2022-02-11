from unittest import TestCase

from mpan.exceptions import InvalidMPANError
from mpan.mpan import MPAN

from .common import INVALID, UNPARSEABLE, VALID


class MPANTestCase(TestCase):
    def test___str__(self):
        self.assertEqual(
            str(MPAN("018011002099999999386")), "018011002099999999386"
        )

    def test___repr__(self):
        self.assertEqual(
            repr(MPAN("018011002099999999386")), "018011002099999999386"
        )

    def test___eq__with_valid_mpans(self):
        for string in VALID:
            self.assertEqual(MPAN(string), MPAN(string))

    def test___eq__with_invalid_mpans(self):
        for string in INVALID:
            self.assertEqual(MPAN(string), MPAN(string))

    def test___eq__with_foreign_objects(self):
        mpan_string = "108011002099999999386"
        self.assertNotEqual(MPAN(mpan_string), mpan_string)
        self.assertNotEqual(MPAN(mpan_string), 108011002099999999386)
        self.assertNotEqual(MPAN(mpan_string), "twelve")

    def test_parsing_long_pass(self):

        mpan = MPAN("018011002099999999386")

        self.assertEqual(mpan.top_line, "01801100")
        self.assertEqual(mpan.profile_class.identifier, "01")
        self.assertEqual(mpan.meter_time_switch_code.identifier, "801")
        self.assertEqual(mpan.line_loss_factor_class, "100")
        self.assertEqual(mpan.core, "2099999999386")
        self.assertEqual(mpan.distributor.identifier, "20")
        self.assertEqual(mpan.identifier, "99999999")
        self.assertEqual(mpan.checksum, "6")

        # Aliases
        self.assertEqual(mpan.pc.identifier, "01")
        self.assertEqual(mpan.mtc.identifier, "801")
        self.assertEqual(mpan.llfc, "100")

    def test_parsing_short_pass(self):

        mpan = MPAN("1099999999997")

        self.assertIsNone(mpan.profile_class)
        self.assertIsNone(mpan.meter_time_switch_code)
        self.assertIsNone(mpan.line_loss_factor_class)
        self.assertEqual(mpan.core, "1099999999997")
        self.assertEqual(mpan.distributor.identifier, "10")
        self.assertEqual(mpan.identifier, "99999999")
        self.assertEqual(mpan.checksum, "7")

        # Aliases
        self.assertIsNone(mpan.pc)
        self.assertIsNone(mpan.mtc)
        self.assertIsNone(mpan.llfc)

    def test_parsing_fail(self):
        for string in UNPARSEABLE:
            with self.subTest(string=string):
                self.assertRaises(InvalidMPANError, MPAN, string)

    def test_is_short(self):
        self.assertTrue(MPAN("1099999999997").is_short)
        self.assertFalse(MPAN("018011002099999999386").is_short)

    def test_is_long(self):
        self.assertFalse(MPAN("1030006718997").is_long)
        self.assertTrue(MPAN("018011002099999999386").is_long)

    def test_as_short(self):
        self.assertEqual(MPAN("1099999999997").as_short, "1099999999997")
        self.assertEqual(
            MPAN("018011002099999999386").as_short, "2099999999386"
        )

    def test_is_valid(self):
        for string in VALID:
            with self.subTest(string=string):
                self.assertTrue(MPAN(string).is_valid)

    def test_is_valid_fail(self):
        for string in INVALID:
            with self.subTest(string=string):
                self.assertFalse(MPAN(string).is_valid)

    def test_check_pass(self):
        for string in VALID:
            with self.subTest(string=string):
                self.assertIsNone(MPAN(string).check())

    def test_check_fail(self):
        for string in INVALID:
            with self.subTest(string=string):
                self.assertRaises(InvalidMPANError, MPAN(string).check)
