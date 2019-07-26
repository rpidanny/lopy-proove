from machine import Pin, Timer


class Proove:
    """
        Packet structure:
        Bit nbr:  Name:
        01-52     Transmitter code. 26 bits, sent as 52 (every other bit is the inverse of previous)
        53-54     Group On(01), Off(10)
        55-56     On(01), Off(10) (or Dim(11)?)
        57-60     Channel. 1=1010, 2=1001, 3=0110, 4=0101
        61-64     Switch.  1=1010, 2=1001, 3=0110, 4=0101

        #                10        20        30        40        50           60
        #       1234567890123456789012345678901234567890123456789012 34 56 7890 1234
        ----------------------------------------------------------------------------
        #1 On:  1010100101101001010101100101011001010101010101010110 10 01 0101 0101
        #1 Off: 1010100101101001010101100101011001010101010101010110 10 10 0101 0101
        #2 On:  1010100101101001010101100101011001010101010101010110 10 01 0101 0110
        #2 Off: 1010100101101001010101100101011001010101010101010110 10 10 0101 0110
        #3 On:  1010100101101001010101100101011001010101010101010110 10 01 0101 1001
        #3 Off: 1010100101101001010101100101011001010101010101010110 10 10 0101 1001
        Gr On:  1010100101101001010101100101011001010101010101010110 01 01 0101 0101
        Gr Off: 1010100101101001010101100101011001010101010101010110 01 10 0101 0101
    """

    tOneHigh = 250  #275
    tOneLow = 250  #170

    tZeroHigh = 250
    tZeroLow = 1250

    tSyncHigh = 250
    tSyncLow = 2500

    tPauseHigh = 250
    tPauseLow = 10000

    _on = "0"
    _off = "1"
    _channel = ["00", "01", "10", "11"]
    _switch = ["00", "01", "10", "11"]

    _num_bits = 26
    _max_int = 67108863

    def __init__(self, gpio=4, tx_repeat=6):
        # self.gpio = gpio
        self.tx_repeat = tx_repeat
        self.tx_pin = Pin(gpio, mode=Pin.OUT)
        self.tx_pin.value(1)

    def close(self):
        print(" [x] Cleanup")

    def _trigger(self,
                 group_state,
                 state_value,
                 switch_id,
                 channel_id=0,
                 transmitter_id=1):
        data = self._encode_transmitter_id(transmitter_id)
        data += group_state
        data += state_value
        data += self._channel[channel_id]
        data += switch_id
        packet = self.encode(data)
        self.tx_packets(packet)

    def encode(self, code):
        data = ""
        for byte in range(0, len(code)):
            data += code[byte]
            if code[byte] == '0':
                data += '1'
            else:
                data += '0'
        return data

    def decode(self, packet):
        data = ""
        for byte in range(0, len(packet) // 2):
            data += packet[byte * 2]
        return data

    def tx_packets(self, packet):
        data = self.decode(packet)
        print(" [x] Data: " + data)
        for _ in range(0, self.tx_repeat):
            print(" [x] Repeat: " + str(_))
            self.tx_packet(packet)

    def tx_packet(self, packet):
        print(" [x] TX packet: " + str(packet))
        self.tx_sync()
        for byte in range(0, len(packet)):
            if packet[byte] == '0':
                self.tx_l0()
            else:
                self.tx_l1()
        self.tx_pause()

    def tx_sync(self):
        self.tx_waveform(self.tSyncHigh, self.tSyncLow)

    def tx_l0(self):
        self.tx_waveform(self.tZeroHigh, self.tZeroLow)

    def tx_l1(self):
        self.tx_waveform(self.tOneHigh, self.tOneLow)

    def tx_pause(self):
        self.tx_waveform(self.tPauseHigh, self.tPauseLow)

    def tx_waveform(self, high_pulse, low_pulse):
        self.tx_pin.value(1)
        Timer.sleep_us(high_pulse)
        self.tx_pin.value(0)
        Timer.sleep_us(low_pulse)

    def _encode_transmitter_id(self, transmitter_id):
        compliment = self._max_int - transmitter_id
        return str("{:>" + str(self._num_bits) + "}").format(
            "{0:b}".format(compliment)).replace(' ', '0')
        # return "{0:b}".format(compliment).zfill(self._num_bits)

    def transmit(self,
                 state,
                 channel,
                 device_id=False,
                 group=False,
                 transmitter_id=1):
        if (group == True):
            self._trigger(self._on if state == True else self._off, self._off,
                          self._switch[device_id], channel, transmitter_id)
        else:
            self._trigger(self._off, self._on if state == True else self._off,
                          self._switch[device_id], channel, transmitter_id)
