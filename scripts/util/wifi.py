import machine
from network import WLAN


def connect_wifi(known_nets):
    wl = WLAN()
    wl.mode(WLAN.STA)
    original_ssid = wl.ssid()
    original_auth = wl.auth()
    print(" [*] Scanning for known wifi nets")
    available_nets = wl.scan()
    print(' [+] Found {} WiFi APs.'.format(len(available_nets)))
    for available_net in available_nets:
        print('     - {} ({})'.format(available_net.ssid, available_net.rssi))
    nets = frozenset([e.ssid for e in available_nets])

    known_nets_names = frozenset([key for key in known_nets])
    net_to_use = list(nets & known_nets_names)
    try:
        net_to_use = net_to_use[0]
        net_properties = known_nets[net_to_use]
        pwd = net_properties['pwd']
        sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
        if 'wlan_config' in net_properties:
            wl.ifconfig(config=net_properties['wlan_config'])
        wl.connect(net_to_use, (sec, pwd), timeout=10000)
        while not wl.isconnected():
            machine.idle()  # save power while waiting
        print(" [+] Connected to " + net_to_use + " with IP address: " +
              wl.ifconfig()[0])

    except Exception as e:
        print(
            " [-] Failed to connect to any known network, going into AP mode")
        wl.init(mode=WLAN.AP,
                ssid=original_ssid,
                auth=original_auth,
                channel=6,
                antenna=WLAN.INT_ANT)
