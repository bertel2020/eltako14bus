"""Optional descriptive metadata adapted to the bertel2020 production API.

Container API derived from grimmpp/eltako14bus at 12df3ca. Field names describe
public properties of this fork; they do not change decoding or validate values.
Wire ranges and enumeration mappings are deliberately omitted pending separate
profile validation. Missing metadata is an error, not a claim of codec support.
"""
from collections import namedtuple
from .eep import EEP

class EEPFieldMetadata(namedtuple(
        "EEPFieldMetadataBase",
        "name description unit value_range values data_type")):
    """Metadata describing one decoded/encoded EEP value.

    ``value_range`` describes the physical or logical value exposed by the
    Python property, not the raw byte range on the wire. ``values`` is useful
    for enumerations and bit fields. The metadata is descriptive; encoding
    and decoding continue to be implemented by the EEP classes themselves.
    """

    __slots__ = ()

    def __new__(cls, name, description="", unit=None, value_range=None,
                values=None, data_type="number"):
        return super(EEPFieldMetadata, cls).__new__(
            cls, name, description, unit, value_range, values, data_type)

    def as_dict(self) -> dict:
        result = {
            "name": self.name,
            "description": self.description,
            "unit": self.unit,
            "value_range": self.value_range,
            "values": dict(self.values) if self.values is not None else None,
            "data_type": self.data_type,
        }
        return result


class EEPMetadata(namedtuple(
        "EEPMetadataBase", "eep name description org fields")):
    """Human- and machine-readable description of an EEP profile."""

    __slots__ = ()

    def __new__(cls, eep, name, description, org, fields=()):
        return super(EEPMetadata, cls).__new__(
            cls, eep, name, description, org, fields)

    def with_eep(self, eep):
        return self._replace(eep=eep)

    def field(self, name: str) -> EEPFieldMetadata:
        """Return metadata for *name* or raise ``KeyError``."""
        for field in self.fields:
            if field.name == name:
                return field
        raise KeyError(name)

    def as_dict(self) -> dict:
        """Return a JSON-friendly representation of this metadata."""
        return {
            "eep": self.eep,
            "name": self.name,
            "description": self.description,
            "org": self.org,
            "fields": [field.as_dict() for field in self.fields],
        }


_METADATA = {
    'F6-01-01': EEPMetadata('F6-01-01', 'one button switch', "Public properties of the production profile.", 5, (
        EEPFieldMetadata('button_pushed', 'Whether the button is pressed.', unit=None, data_type='boolean'),
    )),
    'F6-02-01': EEPMetadata('F6-02-01', '2-part Rocker switch, Application Style 1 (European, bottom switches\non)', "Public properties of the production profile.", 5, (
        EEPFieldMetadata('energy_bow', 'Energy bow flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('rocker_first_action', 'Action of the first rocker.', unit=None, data_type='number'),
        EEPFieldMetadata('rocker_second_action', 'Action of the second rocker.', unit=None, data_type='number'),
        EEPFieldMetadata('second_action', 'Second action flag.', unit=None, data_type='boolean'),
    )),
    'F6-02-02': EEPMetadata('F6-02-02', '2-part Rocker switch, Application Style 2 (US, top switches on)', "Public properties of the production profile.", 5, (
        EEPFieldMetadata('energy_bow', 'Energy bow flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('rocker_first_action', 'Action of the first rocker.', unit=None, data_type='number'),
        EEPFieldMetadata('rocker_second_action', 'Action of the second rocker.', unit=None, data_type='number'),
        EEPFieldMetadata('second_action', 'Second action flag.', unit=None, data_type='boolean'),
    )),
    'F6-10-00': EEPMetadata('F6-10-00', 'Windows handle', "Public properties of the production profile.", 5, (
        EEPFieldMetadata('handle_position', 'Interpreted handle position.', unit=None, data_type='enum'),
        EEPFieldMetadata('movement', 'Raw four-bit movement code.', unit=None, data_type='integer'),
    )),
    'D5-00-01': EEPMetadata('D5-00-01', 'Single input contact', "Public properties of the production profile.", 6, (
        EEPFieldMetadata('contact', 'Contact state.', unit=None, data_type='boolean'),
        EEPFieldMetadata('learn_button', 'Learn button flag.', unit=None, data_type='boolean'),
    )),
    'A5-08-01': EEPMetadata('A5-08-01', 'Light, Temperature and Occupancy sensor', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('current_temperature', 'Measured temperature.', unit='°C', data_type='number'),
        EEPFieldMetadata('illumination', 'Measured illumination.', unit='lx', data_type='number'),
        EEPFieldMetadata('learn_button', 'Learn button flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('occupancy_button', 'Occupancy button flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('pir_status', 'Raw PIR status.', unit=None, data_type='boolean'),
        EEPFieldMetadata('supply_voltage', 'Sensor supply voltage.', unit='V', data_type='number'),
        EEPFieldMetadata('temperature', 'Measured temperature.', unit='°C', data_type='number'),
    )),
    'A5-09-0C': EEPMetadata('A5-09-0C', 'Air quality sensor', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('concentration', 'VOC concentration.', unit=None, data_type='number'),
        EEPFieldMetadata('voc_type', 'Measured VOC substance.', unit=None, data_type='enum'),
        EEPFieldMetadata('voc_unit', 'Concentration unit.', unit=None, data_type='enum'),
    )),
    'A5-09-04': EEPMetadata('A5-09-04', 'CO2, Humidity and Temperature sensor', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('concentration', 'Carbon dioxide concentration.', unit='ppm', data_type='number'),
        EEPFieldMetadata('current_temperature', 'Measured temperature.', unit='°C', data_type='number'),
        EEPFieldMetadata('humidity', 'Relative humidity.', unit='%', data_type='number'),
        EEPFieldMetadata('temperature', 'Measured temperature.', unit='°C', data_type='number'),
    )),
    'A5-38-08': EEPMetadata('A5-38-08', 'Central Command Gateway', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('command', 'Command variant.', unit=None, data_type='enum'),
        EEPFieldMetadata('dimming', 'Dimming command parameters.', unit=None, data_type='object'),
        EEPFieldMetadata('switching', 'Switching parameters: time, switch, delay/duration and optional actuator lock.', unit=None, data_type='object'),
    )),
    'M5-38-08': EEPMetadata('M5-38-08', 'Eltako Gateway Switching - This is implemented pretty rudimentary', "Public properties of the production profile.", 5, (
        EEPFieldMetadata('state', 'Requested switch state.', unit=None, data_type='boolean'),
    )),
    'A5-10-03': EEPMetadata('A5-10-03', 'Thermostat - current and desired temperature', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('current_temperature', 'Current temperature.', unit='°C', data_type='number'),
        EEPFieldMetadata('target_temperature', 'Desired temperature.', unit='°C', data_type='number'),
    )),
    'A5-10-06': EEPMetadata('A5-10-06', 'Heating and Cooling', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('current_temperature', 'Current temperature.', unit='°C', data_type='number'),
        EEPFieldMetadata('mode', 'Heating/cooling operating mode.', unit=None, data_type='enum'),
        EEPFieldMetadata('priority', 'Controller priority.', unit=None, data_type='enum'),
        EEPFieldMetadata('target_temperature', 'Desired temperature.', unit='°C', data_type='number'),
    )),
    'A5-10-12': EEPMetadata('A5-10-12', 'Temperature Controller Command', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('current_temperature', 'Current temperature.', unit='°C', data_type='number'),
        EEPFieldMetadata('humidity', 'Relative humidity.', unit='%', data_type='number'),
        EEPFieldMetadata('target_temperature', 'Desired temperature.', unit='°C', data_type='number'),
    )),
    'A5-13-01': EEPMetadata('A5-13-01', 'Weather station', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('dawn_sensor', 'Dawn/light sensor value.', unit=None, data_type='number'),
        EEPFieldMetadata('day_night', 'Day/night flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('hemisphere', 'Hemisphere flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('identifier', 'Weather telegram variant.', unit=None, data_type='enum'),
        EEPFieldMetadata('learn_button', 'Learn button.', unit=None, data_type='number'),
        EEPFieldMetadata('rain_indication', 'Rain indication.', unit=None, data_type='boolean'),
        EEPFieldMetadata('sun_east', 'East-facing sunlight value.', unit=None, data_type='number'),
        EEPFieldMetadata('sun_south', 'South-facing sunlight value.', unit=None, data_type='number'),
        EEPFieldMetadata('sun_west', 'West-facing sunlight value.', unit=None, data_type='number'),
        EEPFieldMetadata('temperature', 'Measured temperature.', unit='°C', data_type='number'),
        EEPFieldMetadata('wind_speed', 'Wind speed.', unit='m/s', data_type='number'),
    )),
    'A5-04-02': EEPMetadata('A5-04-02', 'Temperature and Humidity Sensor', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('current_temperature', 'Current temperature.', unit='°C', data_type='number'),
        EEPFieldMetadata('humidity', 'Relative humidity.', unit='%', data_type='number'),
        EEPFieldMetadata('learn_button', 'Learn button flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('supply_voltage', 'Supply voltage.', unit='V', data_type='number'),
    )),
    'A5-04-01': EEPMetadata('A5-04-01', 'Temperature and Humidity Sensor', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('current_temperature', 'Current temperature.', unit='°C', data_type='number'),
        EEPFieldMetadata('humidity', 'Relative humidity.', unit='%', data_type='number'),
        EEPFieldMetadata('learn_button', 'Learn button flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('temp_availability', 'Temperature value available.', unit=None, data_type='boolean'),
    )),
    'A5-04-03': EEPMetadata('A5-04-03', 'Temperature and Humidity Sensor', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('current_temperature', 'Current temperature.', unit='°C', data_type='number'),
        EEPFieldMetadata('humidity', 'Relative humidity.', unit='%', data_type='number'),
        EEPFieldMetadata('learn_button', 'Learn button flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('telegram_type', 'Heartbeat or event telegram.', unit=None, data_type='enum'),
    )),
    'A5-12-01': EEPMetadata('A5-12-01', 'Automated Meter Reading - Electricity', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('data_type', 'Meter data type.', unit=None, data_type='integer'),
        EEPFieldMetadata('divisor', 'Decimal divisor code.', unit=None, data_type='integer'),
        EEPFieldMetadata('learn_button', 'Learn button flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('measurement_channel', 'Meter measurement channel.', unit=None, data_type='integer'),
        EEPFieldMetadata('meter_reading', 'Raw cumulative meter reading.', unit=None, data_type='integer'),
    )),
    'A5-12-02': EEPMetadata('A5-12-02', 'Automated Meter Reading - Gas', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('data_type', 'Meter data type.', unit=None, data_type='integer'),
        EEPFieldMetadata('divisor', 'Decimal divisor code.', unit=None, data_type='integer'),
        EEPFieldMetadata('learn_button', 'Learn button flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('measurement_channel', 'Meter measurement channel.', unit=None, data_type='integer'),
        EEPFieldMetadata('meter_reading', 'Raw cumulative meter reading.', unit=None, data_type='integer'),
    )),
    'A5-12-03': EEPMetadata('A5-12-03', 'Automated Meter Reading - Water', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('data_type', 'Meter data type.', unit=None, data_type='integer'),
        EEPFieldMetadata('divisor', 'Decimal divisor code.', unit=None, data_type='integer'),
        EEPFieldMetadata('learn_button', 'Learn button flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('measurement_channel', 'Meter measurement channel.', unit=None, data_type='integer'),
        EEPFieldMetadata('meter_reading', 'Raw cumulative meter reading.', unit=None, data_type='integer'),
    )),
    'G5-3F-7F': EEPMetadata('G5-3F-7F', 'Eltako Shutters', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('direction', 'Movement direction.', unit=None, data_type='integer'),
        EEPFieldMetadata('state', 'Raw shutter state.', unit=None, data_type='integer'),
        EEPFieldMetadata('time', 'Movement time.', unit='s', data_type='integer'),
    )),
    'H5-3F-7F': EEPMetadata('H5-3F-7F', 'Eltako Shutter Command', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('command', 'Shutter command code.', unit=None, data_type='integer'),
        EEPFieldMetadata('learn_button', 'Learn button flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('time', 'Raw movement time byte.', unit=None, data_type='integer'),
    )),
    'A5-07-01': EEPMetadata('A5-07-01', 'Occupancy Sensor', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('learn_button', 'Learn button flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('pir_status', 'Raw PIR status.', unit=None, data_type='integer'),
        EEPFieldMetadata('pir_status_on', 'Whether occupancy is detected.', unit=None, data_type='boolean'),
        EEPFieldMetadata('support_volrage_availability', 'Supply-voltage value available.', unit=None, data_type='boolean'),
        EEPFieldMetadata('support_voltage', 'Support voltage.', unit='V', data_type='number'),
    )),
    'A5-06-01': EEPMetadata('A5-06-01', 'Brightness Twilight Sensor', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('day_light', 'Daylight illumination.', unit='lx', data_type='number'),
        EEPFieldMetadata('illumination', 'Selected illumination value.', unit='lx', data_type='number'),
        EEPFieldMetadata('twilight', 'Twilight threshold/value.', unit='lx', data_type='integer'),
    )),
    'A5-30-01': EEPMetadata('A5-30-01', 'Digital Input with battery status', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('battery_status', 'Raw battery status.', unit=None, data_type='integer'),
        EEPFieldMetadata('contact_closed', 'Whether the contact is closed.', unit=None, data_type='boolean'),
        EEPFieldMetadata('contact_status', 'Raw contact status.', unit=None, data_type='integer'),
        EEPFieldMetadata('learn_button', 'Learn button flag.', unit=None, data_type='boolean'),
        EEPFieldMetadata('low_battery', 'Whether the battery is low.', unit=None, data_type='boolean'),
    )),
    'A5-30-03': EEPMetadata('A5-30-03', 'Digital Inputs', "Public properties of the production profile.", 7, (
        EEPFieldMetadata('digital_input_0', 'Digital input 0.', unit=None, data_type='number'),
        EEPFieldMetadata('digital_input_1', 'Digital input 1.', unit=None, data_type='number'),
        EEPFieldMetadata('digital_input_2', 'Digital input 2.', unit=None, data_type='number'),
        EEPFieldMetadata('digital_input_3', 'Digital input 3.', unit=None, data_type='number'),
        EEPFieldMetadata('learn_button', 'Learn button.', unit=None, data_type='number'),
        EEPFieldMetadata('status_of_wake', 'Status of wake.', unit=None, data_type='number'),
    )),
}


def get_metadata(profile) -> EEPMetadata:
    """Describe an existing profile class, instance or EEP name (hyphen/underscore)."""
    if isinstance(profile, str):
        profile = EEP.find(profile.upper().replace('_', '-'))
    if not isinstance(profile, type):
        profile = type(profile)
    if not issubclass(profile, EEP):
        raise TypeError("Expected an EEP profile, instance or name")
    return _METADATA[profile.eep_string]
