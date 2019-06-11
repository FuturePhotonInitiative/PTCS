from src.Instruments.IEEE_488_2 import IEEE_488_2


class AnritsuMP2100A(IEEE_488_2):

    def __init__(self, device):
        IEEE_488_2.__init__(self, device, "Anritsu MP2100A BERT Analyzer")

    def run_run_all_measurements(self):
        self.device.write("*TRG")

    def run_stop_all_measurements(self):
        self.device.write(":SENSe:MEASure:ASTP")

    def run_set_amplitude(self, amplitude):
        """
        :param amplitude: the amplitude to set, in Vpp
        """
        self.device.query("OUTPut:DATA:AMPLitude " + str(amplitude))

    def run_turn_on_output(self):
        self.device.write(":SOURce:OUTPut:ASET ON")
