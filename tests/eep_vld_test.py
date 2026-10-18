"""VLD (RORG D2) telegrams: variable length and profile decoding."""
import unittest
from eltakobus import eep
from eltakobus.error import WrongOrgError
from eltakobus.message import RegularVLDMessage, Regular4BSMessage

ADDRESS = bytes((0x05, 0x12, 0x34, 0x56))


def bits(*fields):
    """Build a payload from (value, size) fields, MSB first, padded to whole bytes."""
    value, total = 0, 0
    for field, size in fields:
        value = (value << size) | field
        total += size
    total_padded = (total + 7) // 8 * 8
    return (value << (total_padded - total)).to_bytes(total_padded // 8, "big")


class VLDMessageTest(unittest.TestCase):
    def test_keeps_all_data_bytes(self):
        msg = RegularVLDMessage(ADDRESS, 0, bytes(range(10)))
        self.assertEqual(msg.org, 0xD2)
        self.assertEqual(msg.data, bytes(range(10)))

    def test_long_message_cannot_be_serialized_to_esp2(self):
        with self.assertRaises(ValueError):
            RegularVLDMessage(ADDRESS, 0, bytes(10)).body


class D2_14Test(unittest.TestCase):
    def payload(self, contact=0):
        return bits((500, 10), (100, 8), (12345, 17), (1, 2), (500, 10), (0, 10), (1000, 10), (contact, 1), (0, 5))

    def test_d2_14_40(self):
        result = eep.D2_14_40.decode_message(RegularVLDMessage(ADDRESS, 0, self.payload()))
        self.assertAlmostEqual(result.temperature, 10.0)
        self.assertEqual(result.humidity, 50.0)
        self.assertEqual(result.illumination, 12345.0)
        self.assertEqual(result.acceleration_status, 1)
        self.assertAlmostEqual(result.acceleration_x, 0.0)
        self.assertAlmostEqual(result.acceleration_y, -2.5)
        self.assertAlmostEqual(result.acceleration_z, 2.5)

    def test_invalid_values_are_none(self):
        data = bits((1023, 10), (255, 8), (131071, 17), (0, 2), (1023, 10), (1023, 10), (1023, 10), (0, 6))
        result = eep.D2_14_40.decode_message(RegularVLDMessage(ADDRESS, 0, data))
        self.assertIsNone(result.temperature)
        self.assertIsNone(result.humidity)
        self.assertIsNone(result.illumination)
        self.assertIsNone(result.acceleration_x)

    def test_d2_14_41_contact(self):
        for bit in (0, 1):
            result = eep.D2_14_41.decode_message(RegularVLDMessage(ADDRESS, 0, self.payload(contact=bit)))
            self.assertEqual(result.contact, bool(bit))

    def test_short_payload_and_wrong_org(self):
        with self.assertRaises(ValueError):
            eep.D2_14_40.decode_message(RegularVLDMessage(ADDRESS, 0, bytes(4)))
        with self.assertRaises(WrongOrgError):
            eep.D2_14_40.decode_message(Regular4BSMessage(ADDRESS, 0, bytes(4)))


class D2_00_01Test(unittest.TestCase):
    def test_decode(self):
        data = bits((0, 8), (1, 4), (0, 4), (2, 4), (1, 4), (1, 4), (2, 4), (1, 4), (0, 4),
                    (125, 8), (101, 8), (800, 16), (15, 5), (0, 3))
        result = eep.D2_00_01.decode_message(RegularVLDMessage(ADDRESS, 0, data))
        self.assertEqual(result.burglary_alarm, 1)
        self.assertEqual(result.handle_position, 2)
        self.assertEqual(result.window_state, 1)
        self.assertEqual(result.button_right, 1)
        self.assertEqual(result.button_left, 2)
        self.assertEqual(result.motion, 1)
        self.assertAlmostEqual(result.temperature, 20.0)
        self.assertEqual(result.humidity, 50.5)
        self.assertEqual(result.illumination, 800.0)
        self.assertEqual(result.battery_state, 75)

    def test_unsupported_message_type(self):
        with self.assertRaises(eep.NotImplementedError):
            eep.D2_00_01.decode_message(RegularVLDMessage(ADDRESS, 0, bytes((1,) + (0,) * 9)))


if __name__ == "__main__":
    unittest.main()
