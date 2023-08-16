# pythonvicrtonmppt

pythonvictronmppt is a simple python class for reading data sent by victron devices via ve.direct text protocol on a serial port into a dict.

## Installation

```
python setup.py install
```

## Usage

```
import pythonvictronmppt

mppt = pythonvictronmppt("/dev/ttyUSB0", 19200)
data_dict = mppt.read_data()


```
