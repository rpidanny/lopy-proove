# Lopy Proove

Interface with `Proove`/`Anslut`/`Nexa`/`Telldus` remote switches using [LoPy](https://pycom.io) and cheap [433Mhz RF Transmitter](https://www.aliexpress.com/item/32763193655.html).

## Usage

- Make a copy of `scripts/config_example.py` and rename it to `scripts/config.py`
- Fill in your `WiFi credentials`, `MQTT Configs` and `GPIO Pin`.
- Upload the code to LoPy.

The device subscribes to a MQTT topic specified in `scripts/config.py`.

To control the switches, send `JSON String` as message to the topic with the following template:

```json
{
  "on": true,
  "channel": 2,
  "deviceId": 1,
  "transmitter_id": 312312
}
```

## Wiring

| LoPy          | Transmitter   |
| :------------ | :------------ |
| `P8`          | `Data`        |
| `3.3V`        | `VCC`         |
| `GND`         | `GND`         |
