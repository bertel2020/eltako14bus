"""Golden teach-in payloads from the production Home Assistant buttons."""
import unittest
from eltakobus.eep import EEP, A5_10_06
from eltakobus.message import Regular4BSMessage
from eltakobus.teach_in import (build_teach_in_message, get_teach_in_payload,
    supports_teach_in_button, teach_in_devices, teach_in_profiles_for_device,
    teach_in_button_eep_names)

class TeachInTest(unittest.TestCase):
    def test_full_telegrams_match_existing_production_buttons(self):
        address = bytes.fromhex('01020304')
        payloads = {'A5-10-06': '40300D85', 'A5-10-12': '40900D80',
                    'A5-38-08': 'E0400D80', 'H5-3F-7F': 'FFF80D80'}
        self.assertEqual(teach_in_button_eep_names(), sorted(payloads))
        for name, payload in payloads.items():
            with self.subTest(name=name):
                expected = Regular4BSMessage(address=address, data=bytes.fromhex(payload),
                                            outgoing=True, status=0x80)
                for profile in (name, name.lower().replace('-', '_'), EEP.find(name)):
                    actual = build_teach_in_message(address, profile)
                    self.assertEqual(actual.serialize(), expected.serialize())
                    self.assertTrue(actual.outgoing)
                    self.assertEqual(actual.status, 0x80)

    def test_unknown_profiles_are_not_fallbacks(self):
        for profile in ('unknown', 'F6-02-01', None):
            self.assertIsNone(get_teach_in_payload(profile))
            self.assertFalse(supports_teach_in_button(profile))
            with self.assertRaises(ValueError):
                build_teach_in_message(bytes(4), profile)
        self.assertEqual(teach_in_devices('unknown'), ())
        self.assertEqual(teach_in_devices('F6-02-01'), ())

    def test_device_associations_and_returned_copies(self):
        entries = teach_in_profiles_for_device('FSB14')
        self.assertTrue(entries)
        self.assertTrue(all(e['sender_eep'] == 'H5-3F-7F' for e in entries))
        entries[0]['description'] = 'changed'
        self.assertNotEqual(teach_in_profiles_for_device('FSB14')[0]['description'], 'changed')
        self.assertTrue(all(e['sender_eep'] == 'A5-10-06' for e in teach_in_devices(A5_10_06)))
