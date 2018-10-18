# Tektronix CSA8000

### Initialization
The Tektronix CSA8000 uses the GPIB standard for communication and will have an address in the format `GPIB0::16::INSTR`.
The device is implemented as an Object in `CSA8000.py` with the only parameter being a PyVisa device connected to the appropriate address.

---
### Methods

#### Acquire Modes
The CSA8000 supports three modes of data acquisition:
* sample
* average
* envelope

The current mode can be retrieved by calling `run_get_acquisition_param()`
and can be set with `run_set_acquisition_mode(sample, average, envelope)`, where each parameter is of type bool and one, and only one, of them is True

#### Toggling Acquisition
Acquisition can be started by calling `run_start_acquisition()`. It can then later be stopped by calling `run_stop_acquisition()`

#### Sample Rates
The current sample rate can be retrieved by calling `run_get_sample_rate()` or it can be set by calling
`run_set_sample_rate(scale)`, where scale is of type float

####