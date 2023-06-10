
class pythonvictronmppt:

    def __init__(self, serial_port: str = '/dev/ttyUSB0', speed: int = 19200) -> None:
        self.serial_port = serial_port
        self.serial_speed = speed
    
    def read(self):
        """
        Read data from serial console
        """
        


