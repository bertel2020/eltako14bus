"""Protect production telegrams that differ from grimmpp's public API."""
import unittest

from eltakobus.eep import A5_09_04, A5_10_06, F6_02_01
from eltakobus.message import Regular4BSMessage, RPSMessage


class ForkCompatibilityTest(unittest.TestCase):
    def test_rocker_release_keeps_production_payload(self):
        message = F6_02_01(1, 0, 0, 0).encode_message_released(bytes.fromhex('01020304'))
        self.assertIsInstance(message, RPSMessage)
        self.assertEqual(bytes(message.data), b'\x00')
        self.assertEqual(message.status, 0x20)
        self.assertTrue(message.outgoing)

    def test_futh_setpoint_keeps_distinct_wire_format(self):
        message = A5_10_06(1, 20, 20, False).encode_message2(bytes.fromhex('01020304'))
        self.assertEqual(bytes(message.data), bytes.fromhex('00800008'))
        self.assertEqual(message.status, 0)
        self.assertTrue(message.outgoing)

    def test_co2_decoder_keeps_concentration_property(self):
        message = Regular4BSMessage(bytes.fromhex('01020304'), 0, bytes.fromhex('64646408'))
        decoded = A5_09_04.decode_message(message)
        self.assertEqual(decoded.concentration, 1000)
        self.assertEqual(decoded.humidity, 50)
        self.assertEqual(decoded.current_temperature, 20)
