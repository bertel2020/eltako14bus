Eltako14Bus Python library
==========================

This repository contains a library and some tools for interacting with the Eltako Series 14 bus system,
which is an extension to the EnOcean Serial Protocol ESP2.

This is part of the reverse engineering approach that allows using Eltako
Series 14 devices without a FAM.

It can work both on a direct RS485 serial connection to the bus,
with or without a FAM14 present on the bus,
through a FAM14's serial connection,
or through a bespoke CoAP interface to the ESP2 protocol.

Tools
-----

The eltakotool program shipped with it can
do various raw interactions with the bus
(replacing some FAM14 functionality, locking and unlocking the bus, sending arbitrary messages)
as well as reading and writing the bus participants' memory
(including verification and annotation of the memory contents).

Protocol description
--------------------

(This is a short version.
The long is partially available in the EnOcean and Eltako documentations,
and the rest is in the reverse engineered code).

The EnOcean serial protocol is a point-to-point serial protocol between a computer and a radio transceiver;
it contains synchronization bytes, some structured data bytes, and checksumming.
The most common message formats are RPS and 4BS,
which have equivalent messages (with short and long (4 byte) data, respectively) on the radio side.
These messages contain some addressing information both when receiving (indicating which device sent it)
and when sending through the transceiver (in which case the addresses need to match the address range of the transceiver, giving about 128 possible sending addresses).

The Eltako protocol is loosely built on the ESP2 protocol,
but is used on an RS485 bus (with up to 127 participants),
and uses several message types that are not defined in ESP2.

Part of the Eltako bus protocol is enumeration:
Devices on the bus can be put into an addressing mode,
and the bus master (a FAM14 or the library user) can assign one of the 127 available address to the device.

Commands are also known to visually identify devices on the bus,
and to read and write their configuration (eg. in a relay, setting which buttons it should react to).

License
-------

This was developed by Christian Amsüss <c.amsuess@energyharvesting.at> and Energy Harvesting Solutions 2016-2020.

It is published under the terms of GNU LGPL version 3 or later.


## Optional catalog, metadata and teach-in helpers

These APIs are additive and do not configure devices or transmit telegrams.
Catalog data and helper/container APIs originate from grimmpp/eltako14bus
(commit `12df3caa923811ff6323746e238bc7d099608428`), adapted for this fork.

```python
from eltakobus.device_catalog import describe_hw_type, get_device_templates
from eltakobus.eep_metadata import get_metadata
from eltakobus.teach_in import build_teach_in_message

info = describe_hw_type("FSR14_4x")
templates = get_device_templates("light")
metadata = get_metadata("A5-09-04")  # or EEP.find("A5-09-04").get_metadata()
message = build_teach_in_message(bytes.fromhex("01020304"), "A5-38-08")
```

The full catalog also describes devices with profiles this fork does not yet
implement. Configuration templates exclude those profiles; a catalog row is not
proof of hardware validation or automatic Home Assistant support. Applications
should pass their own supported EEP lists when requesting templates.

Metadata describes the public properties of this fork, including `concentration`
for CO2 and `supply_voltage` for A5-04-02. It intentionally omits unvalidated ranges
and enumeration mappings. It neither changes nor validates codec behavior.

Teach-in helpers preserve the four payloads/status/outgoing flag used by the
existing Home Assistant buttons. Building a message does not send it. Unsupported
profiles return no payload and `build_teach_in_message` raises `ValueError`.
Existing Home Assistant buttons and configuration remain independent of these APIs.
