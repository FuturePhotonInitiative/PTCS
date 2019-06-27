import time

from src.Instruments.PyVisaDriver import PyVisaDriver


class Keithley2280S(PyVisaDriver):
    """
    This class models a Keithley 2280S Power Supply
    """

    def __init__(self, device):
        PyVisaDriver.__init__(self)
        self.name += "Keithley 2280S Power Supply"
        self.device = device

    def run_get_voltage(self, channel=1):
        channel = str(channel)
        self.device.write(':SENS' + channel + ':FUNC "VOLT')
        self.device.write(':TRAC:CLE')
        time.sleep(0.3)
        return float(self.device.query(':DATA' + channel + ':DATA? "READ,UNIT"').split(',')[0][:-1])

    def run_get_current(self, channel=1):
        channel = str(channel)
        self.device.write(':SENS' + channel + ':FUNC "CURR"')
        self.device.write(':TRAC:CLE')
        time.sleep(0.3)
        return float(self.device.query('DATA' + channel + ':DATA? "READ,UNIT"').split(',')[0][:-1])

    def run_set_voltage(self, voltage=0, channel=1):
        voltage = str(voltage)
        channel = str(channel)
        self.device.write(':SOUR' + channel + ':VOLT ' + voltage)

    def run_set_current(self, current=0, channel=1):
        current = str(current)
        channel = str(channel)
        self.device.write(':SOUR' + channel + ':CURR ' + current)

    def run_set_over_voltage(self, voltage=0, channel=1):
        voltage = str(voltage)
        channel = str(channel)
        self.device.write(':SOUR' + channel + ':VOLT:PROT ' + voltage)

    def run_set_over_current(self, current=0, channel=1):
        current = str(current)
        channel = str(channel)
        self.device.write(':SOUR' + channel + ':CURR:PROT ' + current)

    def run_set_output_switch(self, value=0, channel='CH1'):
        value = str(value)
        channel = str(channel)
        self.device.write('OUTP ' + value + ',' + channel)

    def run_get_set_voltage(self, channel=1):
        channel = str(channel)
        return self.device.query(':SOUR' + channel + ':VOLT?')

    def run_get_set_current(self, channel=1):
        channel = str(channel)
        return self.device.query(':SOUR' + channel + ':CURR?')

    def run_get_out_switch(self):
        return self.device.query('OUTP?')

    def run_save_state(self, slot=1):
        self.device.write('*SAV ' + str(slot))

    def run_recall_state(self, slot=1):
        self.device.write('*RCL ' + str(slot))
