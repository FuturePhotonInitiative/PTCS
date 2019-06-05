from EVTPyVisaDriver import EVTPyVisaDriver


class Newport835(EVTPyVisaDriver):

    INCLUDE_UNITS = "G0"
    SUPPRESS_UNITS = "G1"

    def __init__(self, device):
        EVTPyVisaDriver.__init__(self, device, "Newport 835 Optical Power Meter")

        # Each command needs to end with a 'X' to be executed and for the device to be ready for another command.
        # More than one command per command string is possible, but it is cleaner to not.
        self.device.write_termination = 'X' + self.device.write_termination

        # Every time device.write("X") is done, the instrument will return one power reading.
        self.device.write("T5")

        # The attenuator (the cap placed on the light sensor) is on.
        # If you want to take the attenuator off, than this should be changed to "A0".
        # Taking the attenuator off is only helpful in low light scenarios.
        self.device.write("A1")

        # Used for setting the reading units. one can set these discrete watt ranges. nano, micro, milli.
        # "auto" sets a good range depending on the amount of light detected. This is the default.
        self.unit_switch = {
            "auto": "R0",
            "2nW": "R1",
            "20nW": "R2",
            "200nW": "R3",
            "2uW": "R4",
            "20uW": "R5",
            "200uW": "R6",
            "2mW": "R7",
            "20mW": "R8",
            "200mW": "R9",
            "2W": "R10",
            "20W": "R11"
        }

    def run_get_wavelength(self, units=False):
        """
        :param units: do you want nm at the end?
        :return: the wavelength being detected
        """
        self.device.write(Newport835.INCLUDE_UNITS if units else Newport835.SUPPRESS_UNITS)
        return self.device.query("U1")

    def run_set_wavelength(self, wavelength):
        """
        :param wavelength: the 4 digit wavelength in nm. This value is rounded to the nearest power of 10
        """
        self.device.write("W+" + wavelength)

    def run_get_power(self, units=False):
        """
        :param units: do you want detected units at the end?
        :return: a power reading from the instrument at the time called
        """
        self.device.write(Newport835.INCLUDE_UNITS if units else Newport835.SUPPRESS_UNITS)
        return self.device.query("X")

    def run_change_reading_units(self, how_many_watts):
        """
        :param how_many_watts: the amount of watts to set the unit to detect.
        This could be auto, (2, 20, 200) nW, (2, 20, 200) uW, (2, 20, 200) mW, (2, 20) W
        """
        self.device.write(self.unit_switch[how_many_watts])
