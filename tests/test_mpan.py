import json

from pathlib import Path
from unittest import TestCase

from mpan import (
    MPAN,
    Distributor,
    InvalidMPANError,
    MeterTimeSwitchCode,
    ProfileClass,
    is_valid,
)


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


class DistributorTestCase(TestCase):
    def setUp(self):
        self.dno = Distributor(identifier="10")
        self.idno = Distributor(identifier="24")

    def test___str__(self):
        self.assertEqual(str(self.dno), "10")
        self.assertEqual(str(self.idno), "24")

    def test___repr__(self):
        self.assertEqual(repr(self.dno), "Distributor: 10")
        self.assertEqual(repr(self.idno), "Distributor: 24")

    def test___bool__(self):
        self.assertTrue(Distributor(identifier="10"))
        self.assertTrue(Distributor(identifier="24"))
        self.assertFalse(Distributor(identifier="test"))

    def test_is_valid(self):
        self.assertTrue(self.dno.is_valid)
        self.assertTrue(self.idno.is_valid)
        self.assertFalse(
            Distributor(identifier="99").is_valid  # The Great One 🇨🇦 🏒
        )
        self.assertFalse(Distributor(identifier="test").is_valid)

    def test_area(self):
        self.assertEqual(self.dno.area, "Eastern England")
        self.assertIsNone(self.idno.area)

    def test_operator(self):
        self.assertEqual(self.dno.operator, "UK Power Networks")
        self.assertIsNone(self.idno.operator)

    def test_participant_id(self):
        self.assertEqual(self.dno.participant_id, "EELC")
        self.assertIsNone(self.idno.participant_id)

    def test_gsp_group_id(self):
        self.assertEqual(self.dno.gsp_group_id, "_A")
        self.assertIsNone(self.idno.gsp_group_id)

    def test_name(self):
        self.assertIsNone(self.dno.name)
        self.assertEqual(self.idno.name, "Envoy")

    def test_licensee(self):
        self.assertIsNone(self.dno.licensee)
        self.assertEqual(self.idno.licensee, "Independent Power Networks")

    def test_mpas_operator_id(self):
        self.assertIsNone(self.dno.mpas_operator_id)
        self.assertEqual(self.idno.mpas_operator_id, "IPNL")

    def test_is_dno(self):
        self.assertTrue(self.dno.is_dno)
        self.assertFalse(self.idno.is_dno)

    def test_is_idno(self):
        self.assertFalse(self.dno.is_idno)
        self.assertTrue(self.idno.is_idno)


class ProfileClassTestCase(TestCase):
    def setUp(self):
        self.pc = ProfileClass(identifier="04")

    def test_is_valid(self):
        self.assertTrue(self.pc)
        self.assertFalse(ProfileClass(identifier="test"))

    def test_description(self):
        self.assertEqual(self.pc.description, "Non-domestic Economy 7")
        self.assertEqual(ProfileClass("").description, None)


class MeterTimeSwitchCodeTestCase(TestCase):
    def test_is_valid(self):
        self.assertTrue(MeterTimeSwitchCode("001"))
        self.assertTrue(MeterTimeSwitchCode("999"))
        self.assertFalse(MeterTimeSwitchCode("1000"))
        self.assertFalse(MeterTimeSwitchCode("0"))
        self.assertFalse(MeterTimeSwitchCode("00"))
        self.assertFalse(MeterTimeSwitchCode("000"))
        self.assertFalse(MeterTimeSwitchCode("-1"))
        self.assertFalse(MeterTimeSwitchCode("test"))

    def test_description(self):
        self.assertEqual(MeterTimeSwitchCode("404").description, "Reserved")
        self.assertEqual(MeterTimeSwitchCode("").description, None)
        self.assertEqual(MeterTimeSwitchCode("1000").description, None)
        self.assertEqual(MeterTimeSwitchCode("test").description, None)


class MPANTestCase(TestCase):
    def test___str__(self):
        self.assertEqual(
            str(MPAN("018011002099999999386")), "018011002099999999386"
        )

    def test___repr__(self):
        self.assertEqual(
            repr(MPAN("018011002099999999386")), "018011002099999999386"
        )

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
        for string in get_valid_mpans():
            with self.subTest(string=string):
                self.assertTrue(MPAN(string).is_valid)

    def test_is_valid_fail(self):
        for string in INVALID:
            with self.subTest(string=string):
                self.assertFalse(MPAN(string).is_valid)

    def test_check_pass(self):
        for string in get_valid_mpans():
            with self.subTest(string=string):
                self.assertIsNone(MPAN(string).check())

    def test_check_fail(self):
        for string in INVALID:
            with self.subTest(string=string):
                self.assertRaises(InvalidMPANError, MPAN(string).check)


class IsValidTestCase(TestCase):
    def test_is_valid(self):
        for string in get_valid_mpans():
            with self.subTest(string=string):
                self.assertTrue(is_valid(string), string)

    def test_is_valid_fail(self):
        for string in INVALID:
            with self.subTest(string=string):
                self.assertFalse(is_valid(string))
        for string in UNPARSEABLE:
            with self.subTest(string=string):
                self.assertFalse(is_valid(string))
