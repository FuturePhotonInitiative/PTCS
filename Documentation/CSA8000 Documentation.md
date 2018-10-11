# Tektronix CSA8000


### Initialization
The Tektronix CSA8000 uses the GPIB standard for communication and will have an address in the format `GPIB0::16::INSTR`.
The device is implemented as an Object in `CSA8000.py` with the only parameter being a PyVisa device connected to the appropriate address.

