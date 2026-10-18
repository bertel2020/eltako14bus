"""Metadata follows production properties, including fork-specific names."""
import json
import unittest
from eltakobus import eep
from eltakobus.eep_metadata import get_metadata

class EEPMetadataTest(unittest.TestCase):
    def test_every_profile_describes_exactly_its_public_properties(self):
        for cls in vars(eep).values():
            if not isinstance(cls, type) or not hasattr(cls, 'eep_string'):
                continue
            metadata = cls.get_metadata()
            self.assertEqual(metadata.eep, cls.eep_string)
            actual = {n for n in dir(cls) if isinstance(getattr(cls, n), property)}
            self.assertEqual({f.name for f in metadata.fields}, actual)
            json.dumps(metadata.as_dict())

    def test_production_variants(self):
        co2 = get_metadata('a5_09_04')
        self.assertEqual(co2.field('concentration').unit, 'ppm')
        with self.assertRaises(KeyError):
            co2.field('co2')
        self.assertEqual(get_metadata(eep.A5_04_02).field('supply_voltage').unit, 'V')
        self.assertIsNotNone(get_metadata(eep.A5_30_03).field('digital_input_3'))
        with self.assertRaises(KeyError):
            get_metadata('D2-14-40')

    def test_serialization_does_not_expose_container_state(self):
        metadata = get_metadata(eep.A5_10_06)
        metadata.as_dict()['fields'].clear()
        self.assertTrue(metadata.fields)
