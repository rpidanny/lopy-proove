# boot.py -- run on boot-up
import os
import machine
from config import known_nets
from util.wifi import connect_wifi

uart = machine.UART(0, 115200)
os.dupterm(uart)

if machine.reset_cause() != machine.SOFT_RESET:
	connect_wifi(known_nets)
