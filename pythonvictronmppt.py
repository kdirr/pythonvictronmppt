import serial


class pythonvictronmppt:

    def __init__(self, serial_port: str = '/dev/ttyUSB0', speed: int = 19200) -> None:
        self.serial_port = serial_port
        self.serial_speed = speed
    
    

    def get_data(self):
        """
        reads data from the serial port the solar charge controller is connected to and filters it after given regex.
        returns a match object if the regex matched or none if not.
        """
        with serial.Serial(self.serial_port, self.serial_speed, timeout=None, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE) as s:
            result = None
            while not result:
                result = self.read_serial(s)
                

    def read_serial(self, conn):
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


