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
    byte_counter = 0
    msg = b''
    start = False
    while True:
        byte = conn.read()
        for b in byte:
            byte_counter += b
        msg += byte
        #print(s.readline())
        if start == False and msg.endswith(b'\r\n'):
            msg = b''
            #byte_counter = 0
            start = True
        if msg.endswith(b'Checksum\t'):
            print("found checksum")
            #msg = msg.removesuffix(b'\r\nChecksum\t')
            byte = conn.read()
            for b in byte:
                byte_counter += b
            msg += byte
            break

    checksum = byte_counter % 256
    print(checksum)
    print(msg)
    if checksum == 0:
        return msg
    else:
        return None

get_data()