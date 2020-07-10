known_nets = {
    '<net>': {
        'pwd': '<password>'
    },
    '<net>': {
        'pwd': '<password>',
        'wlan_config': ('10.0.0.114', '255.255.0.0', '10.0.0.1', '10.0.0.1')
    },  # (ip, subnet_mask, gateway, DNS_server)
}

gpio_config = {
    'tx_pin': 'P9'
}

mqtt_config = {
    'host': '192.168.2.10',
    'port': 1883,
    'subscription_topic': '/control/devices/proove'
}
