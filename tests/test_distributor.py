from unittest import TestCase

from freezegun import freeze_time

from mpan.distributor import Distributor


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

    def test_participant_id(self):
        self.assertEqual(self.dno.participant_id, "EELC")
        self.assertEqual(self.idno.participant_id, "IPNL")

    def test_gsp_group_ids(self):

        distributor = Distributor(identifier="28")

        with freeze_time("2001-01-01"):
            self.assertEqual(distributor.gsp_group_ids, [])

        with freeze_time("2010-01-01"):
            self.assertEqual(distributor.gsp_group_ids, ["_C"])

        with freeze_time("2020-01-01"):
            self.assertEqual(distributor.gsp_group_ids, [])

    def test_name(self):
        self.assertEqual(self.dno.name, "UK Power Networks")
        self.assertEqual(self.idno.name, "Independent Power Networks Ltd.")

    def test_type(self):
        self.assertEqual(self.dno.type, "DNO")
        self.assertEqual(self.idno.type, "IDNO")

    def test_is_dno(self):
        self.assertTrue(self.dno.is_dno)
        self.assertFalse(self.idno.is_dno)

    def test_is_idno(self):
        self.assertFalse(self.dno.is_idno)
        self.assertTrue(self.idno.is_idno)
