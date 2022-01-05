from unittest import TestCase

from mpan.meter_time_switch_code import MeterTimeSwitchCode


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
