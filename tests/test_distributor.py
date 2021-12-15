from unittest import TestCase

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
