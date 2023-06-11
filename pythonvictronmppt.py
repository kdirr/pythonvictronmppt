import serial


class pythonvictronmppt:

    def __init__(self, serial_port: str = '/dev/ttyUSB0', speed: int = 19200) -> None:
        self.serial_port = serial_port
        self.serial_speed = speed
        self.raw_msg = None
        self.max_retries = 10
    
    

    def read_data(self):
        """
        reads data from the serial port the solar charge controller is connected to.
        """
        with serial.Serial(self.serial_port, self.serial_speed, timeout=None, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE) as s:
            counter = 0
            while not self.raw_msg:
                self.raw_msg = self._read_serial_data(s)
                counter += 1
                if counter >= self.max_retries:
                    break


    def _read_serial_data(self, conn):
        byte_sum = 0
        msg = b''
        msg_start = False
        msg_stop = False

        while not msg_stop:
            # stop reading when reaching checksum field
            if msg.endswith(b'Checksum\t'):
                msg_stop = True

            # read single byte and append it to msg
            byte = conn.read()
            msg += byte

            # necessary for whatever reason
            for b in byte:
                byte_sum += b

            # reset recorded msg when message starts (on first newline)
            if msg_start == False and msg.endswith(b'\r\n'):
                msg = b''
                msg_start = True

        # calculate checksum
        if (byte_sum % 256) == 0:
            return msg
        else:
            return None
    
    def _dict_from_raw_data(self, raw_data: bytes):
        """
        converts the given raw data from MPPT controller into a dictionary
        """
        data_dict = {}
        lines = raw_data.splitlines()
        for line in lines:
            key_value = line.split(b'\t')
            data_dict[key_value[0].decode('cp1252')] = key_value[1].decode('cp1252')
        return data_dict


