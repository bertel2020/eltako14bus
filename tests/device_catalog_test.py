"""Catalog lookups must not advertise missing codecs or mutate shared data."""
import unittest
from eltakobus.eep import EEP
from eltakobus.device_catalog import (describe_hw_type, find_hw_type,
    describe_gateway_type, entries_for_hw_type, get_device_templates)

class DeviceCatalogTest(unittest.TestCase):
    def test_lookup_returns_copies(self):
        for lookup, name in ((describe_hw_type, 'FUD14'), (find_hw_type, 'FUD14'),
                             (describe_gateway_type, 'fam14')):
            original = lookup(name)
            lookup(name)['description'] = 'changed'
            self.assertEqual(lookup(name), original)

    def test_all_offered_templates_have_existing_codecs(self):
        for platform in ('sensor', 'binary_sensor', 'light', 'climate', 'cover'):
            for entry in get_device_templates(platform):
                EEP.find(entry['eep'])
                if entry.get('sender_eep'):
                    EEP.find(entry['sender_eep'])
        self.assertIn('D2-14-40', [e['eep'] for e in get_device_templates('sensor')])

    def test_channel_counts_and_profile_filter(self):
        self.assertEqual(describe_hw_type('FSR14_4x')['address_count'], 4)
        self.assertGreater(len(entries_for_hw_type('FTS14EM')), 1)
        templates = get_device_templates('light', supported_eeps=['A5-38-08'])
        self.assertTrue(templates)
        self.assertTrue(all(t['eep'] == 'A5-38-08' for t in templates))
