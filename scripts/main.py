# main.py -- put your code here!
import time
import json
from machine import WDT
from network import WLAN

from mqtt import MQTTClient
from proove import Proove

from config import known_nets, gpio_config, mqtt_config
from util.wifi import connect_wifi

wdt = WDT(timeout=2000)

wl = WLAN()

# TODO: Generate unique random Client ID
client = MQTTClient("lopy-proove",
                    server=mqtt_config['host'],
                    port=mqtt_config['port'])


def on_message(topic, msg):
    print(" [+] " + str(topic) + " " + str(msg))

    payload = msg.decode('utf-8')

    data = json.loads(payload)

    proove_remote.transmit(state=data['on'],
                           channel=data['channel'],
                           device_id=data['deviceId'],
                           transmitter_id=data['transmitterId'])


if __name__ == "__main__":
    proove_remote = Proove(gpio_config['tx_pin'])

    client.set_callback(on_message)

    client.connect()

    client.subscribe(topic=mqtt_config['subscription_topic'])

    print(' [*] Waiting for messages...')
    while True:
        try:
            client.check_msg()
        except:
            print(' [-] Failed to ping....')
            print(' [*] Reconnecting to WIFI / MQTT.')
            connect_wifi(known_nets)
            client.connect()
        wdt.feed()
        time.sleep(0.1)
