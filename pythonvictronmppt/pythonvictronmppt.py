'''
 # @ Author: Konstantin Dirr
 # @ Create Time: 2023-06-10
 '''

import serial


class pythonvictronmppt:
    """
    Simple python class for reading data sent via ve.direct serial protocol into a dict.

    To do so, simply create an instance and run instance.read_data()
    """

    def __init__(self, serial_port: str = '/dev/ttyUSB0', speed: int = 19200) -> None:
        self.serial_port = serial_port
        self.serial_speed = speed
        self.raw_msg = None
        self.msg = None
    
    

    def read_data(self, max_retries=10):
        """
        read one message block from the connected device.

        Returns
        -------
        None 
            if no valid message is retrieved after more than x retries
        dict 
            if valid message was received
        """
        with serial.Serial(self.serial_port, self.serial_speed, timeout=None, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE) as s:
            counter = 0
            while not self.raw_msg:
                self.raw_msg = self._read_serial_data(s)
                counter += 1
                if self.raw_msg:
                    self.msg = self._dict_from_raw_data(self.raw_msg)
                    return self.msg
                if counter >= max_retries:
                    return None
                    


    def _read_serial_data(self, conn):
        """
        Read raw data from serial connection

        Parameters
        ----------
        conn : Serial
            Serial port connection

        Returns
        -------
        None
            If checksum of retrieved message is not valid.
        bytes
            Entire message as bytes if the checksum was valid.
        """
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
        converts the given raw data from _read_serial_data() into a dictionary

        Parameters
        ----------
        raw_data : bytes
            bytes containing the message from Solar Charger

        Returns
        -------
        dict
            dict with all keys and values as strings
        """
        data_dict = {}
        lines = raw_data.splitlines()
        for line in lines:
            key_value = line.split(b'\t')
            if key_value[0] == b'Checksum':
                continue
            else:
                data_dict[key_value[0].decode('cp1252')] = key_value[1].decode('cp1252')
        return data_dict


