import unittest
from pythonvictronmppt import pythonvictronmppt
from unittest.mock import Mock

class TestSerialReader(unittest.TestCase):
    def setUp(self) -> None:
        self.test_data = []
        with open("test_data.txt", mode="rb") as test_data_file:
            byte = test_data_file.read(1)
            while byte:
                self.test_data.append(byte)
                byte = test_data_file.read(1)
        
        self.test_result = b'PID\t0xA042\r\nFW\t159\r\nSER#\tHQ212737MMQ\r\nV\t13730\r\nI\t500\r\nVPV\t40920\r\nPPV\t14\r\nCS\t5\r\nMPPT\t1\r\nERR\t0\r\nLOAD\tON\r\nIL\t500\r\nH19\t16694\r\nH20\t37\r\nH21\t97\r\nH22\t37\r\nH23\t88\r\nHSDS\t125\r\nChecksum\ta'


        
    def test_read_serial_data(self):
        m = Mock()
        m.read.side_effect = self.test_data

        mppt_reader = pythonvictronmppt()

        result = None
        while not result:
            result = mppt_reader._read_serial_data(m)

        m.assert_called()
        self.assertEqual(result, self.test_result)

if __name__ == '__main__':
    unittest.main()