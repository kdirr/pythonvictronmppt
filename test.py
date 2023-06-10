import serial

def get_data(serial_port="/dev/ttyUSB0", serial_speed=19200, lines_to_read=20, timeout=1):
    """
    reads data from the serial port the solar charge controller is connected to and filters it after given regex.
    returns a match object if the regex matched or none if not.
    """
    with serial.Serial(serial_port, serial_speed, timeout=None, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE) as s:
        result = None
        while not result:
            result = read_serial(s)

def read_serial(conn):
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
        
        # reset recorded msg on message start
        if msg_start == False and msg.endswith(b'\r\n'):
            msg = b''
            msg_start = True

    # calculate checksum
    checksum = byte_sum % 256

    if checksum == 0:
        return msg
    else:
        return None

get_data()