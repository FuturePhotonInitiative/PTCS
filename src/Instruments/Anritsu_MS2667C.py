from src.Instruments.PyVisaDriver import PyVisaDriver


class Anritsu_MS2667C(PyVisaDriver):
    """
    This class models an Anritsu MS2667C Spectrum Analyzer
    """

    def __init__(self, device):
        PyVisaDriver.__init__(self)
        self.name += "Anritsu MS2667C Spectrum Analyzer"
        self.device = device

    def waveform_read_central(self, central, span, resolution_step=1):
        self.device.write('CF %dMHZ' % central)
        self.device.write('SP %dMHZ' % span)
        self.device.write('TS')

        self.device.write('BIN 0')

        values = []
        for count in range(0, 500, resolution_step):
            values.append(float(self.device.query('XMA? %d, %d' % (count, resolution_step))))

        return values

    def waveform_read_range(self, start, end, resolution_step=1):
        self.device.write('FA %dMHZ' % start)
        self.device.write('FB %dMHZ' % end)
        self.device.write('TS')

        self.device.write('BIN 0')

        values = []

        for count in range(0, 500, resolution_step):
            values.append(float(self.device.query('XMA? %d %d' % (count, resolution_step))))

        return values

    def get_peak(self, central, span):
        self.device.write('CF %dMHZ' % central)
        self.device.write('SP %dMHZ' % span)
        self.device.write('TS')

        self.device.write('MKR 0')
        self.device.write('MKPK')
        peak_frequency = float(self.device.query('MKF?'))

        level = float(self.device.query('MKL?'))

        return peak_frequency, level
