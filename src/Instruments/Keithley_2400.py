from src.Instruments.PyVisaDriver import PyVisaDriver


class Keithley_2400(PyVisaDriver):
    """
    This class models a Keithley 2400 Source Meter
    """

    def __init__(self, device):
        PyVisaDriver.__init__(self)
        self.name += "Keithley 2400 Source Meter"
        self.device = device

    def get_voltage(self, query_range=10, resolution=0.01):
        query_range = str(query_range)
        resolution = str(resolution)
        return float(self.device.query(':MEAS:VOLT:DC?' + query_range + ',' + resolution))

    def get_current(self, query_range=1, resolution=0.000001):
        query_range = str(query_range)
        resolution = str(resolution)
        return float(self.device.query(':MEAS:CURR:DC?' + query_range + ',' + resolution))

    def set_voltage(self, voltage=0):
        self.device.write(':SOUR:FUNC VOLT')
        self.device.write(':SOUR:VOLT ' + str(voltage))

    def set_current(self, current=0):
        self.device.write(':SOUR:FUNC CURR')
        self.device.write(':SOUR:CURR ' + str(current))

    def set_over_voltage(self, voltage=0):
        self.device.write(':SENS:VOLT:PROT ' + str(voltage))

    def set_over_current(self, current=0):
        self.device.write(':SENS:CURR:PROT ' + str(current))

    def set_output_switch(self, state=False):
        self.device.write(':OUTP ' + 'ON' if state else 'OFF')

    def get_set_voltage(self):
        return self.device.query(':SOUR:VOLT?')

    def get_set_current(self):
        return self.device.query(':SOUR:CURR?')

    def get_output_switch(self):
        return self.device.query(':OUTP?')

    def save_state(self, slot=1):
        self.device.write('*SAV ' + str(slot))

    def recall_state(self, slot=1):
        self.device.write('*RCL ' + str(slot))
