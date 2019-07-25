# main.py -- put your code here!
import time
import json
from machine import WDT
from network import WLAN

from mqtt import MQTTClient
from proove import Proove

from config import known_nets, tx_pin
from util.wifi import connect_wifi

wdt = WDT(timeout=60000)

wl = WLAN()

client = MQTTClient(
    "lopy-proove",
    "192.168.2.10",
    port=1883)

def on_message(topic, msg):
    print(" [+] " + str(topic) + " " + str(msg))

    payload = msg.decode('utf-8')

    data = json.loads(payload)

    proove_remote.transmit(state=data['on'],
                           channel=data['channel'],
                           device_id=data['deviceId'],
                           transmitter_id=data['transmitterId'])

if __name__ == "__main__":
    proove_remote = Proove(tx_pin)

    client.set_callback(on_message)

    client.connect()

    client.subscribe(topic="/control/devices/proove")

    while True:
        client.check_msg()
        try:
            client.ping()
        except:
            print(' [-] Failed to ping....')
            print(' [*] Reconnecting to WIFI / MQTT.')
            connect_wifi(known_nets)
            client.connect()
        wdt.feed()
        time.sleep(0.4)
