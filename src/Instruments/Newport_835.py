from src.Instruments.Prologix_GPIBtoUSBController import Prologix_GPIBtoUSBController

# the termination character sequence necessary for an instrument to read a command
TERM_SEQUENCE = "X"


class Newport_835(Prologix_GPIBtoUSBController):
    """
    This class models a Newport 835 Optical Power Meter

    Please use the _send_to_device and _query_device instead of device.write and query for this device. Weird
    things happen with the fact that the GPIB to USB converter has a read-after-write setting that does not always
    work well with device.read and device.query

    Dont forget that if the attenuator cap is screwed on the detector, you should run the command
    to let the instrument know that it is on. This is not the default when turned on.
    """

    def __init__(self, device):
        Prologix_GPIBtoUSBController.__init__(self)
        self.name += "Newport 835 Optical Power Meter"
        self.device = device
        self._become_controller()

        # Make sure this is set with the same binary number of the back of the instrument
        self.instrument_gpib_address = 1

        # The instrument naturally outputs a \r\n, so lets make VISA think that is part of the termination char sequence
        self.device.read_termination = "\r\n"

        # The default setting is for the instrument to give back a power reading when the GPIB read command is sent
        # this could be problematic because read commands are sent all the time and commands could get off and you can
        # receive a power reading when you asked for something else accidentally. Making an 'X' be the command is more
        # accurate at producing power readings when expected and not when not expected.
        self.set_get_power_reading_on_x()

        # I am not sure what the four characters before a power reading stand for, but they are annoying anyway
        self.make_outputs_unverbose()

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

    def check_connected(self):
        try:
            self.get_wavelength()
            return True
        except Exception:
            return False

    def get_wavelength(self):
        """
        :return: the wavelength being detected in the form WAVE[n]nnn
        """
        return self._query_device("U1", TERM_SEQUENCE)

    def turn_off_attenuator(self):
        self._send_to_device("A0", TERM_SEQUENCE)

    def turn_on_attenuator(self):
        """
        Lets the instrument know that the attenuator cap is on the light sensor so readings are correct
        """
        self._send_to_device("A1", TERM_SEQUENCE)

    def set_wavelength(self, wavelength):
        """
        :param wavelength: the wavelength in nm. This value is rounded to the nearest power of 10
        """
        self._send_to_device("W+{}".format(wavelength), TERM_SEQUENCE)

    def set_get_power_reading_on_x(self):
        """
        :return: Every time an "X" is sent alone to the instrument it will give back a power reading
        """
        self._send_to_device("T4", TERM_SEQUENCE)

    def get_power_reading(self):
        """
        :return: a power reading from the instrument at the time called
        """
        return self._query_device("", TERM_SEQUENCE)

    def change_reading_units(self, how_many_watts):
        """
        :param how_many_watts: the amount of watts to set the unit to detect.
        This could be auto, (2, 20, 200) nW, (2, 20, 200) uW, (2, 20, 200) mW, (2, 20) W
        """
        self._send_to_device(self.unit_switch[how_many_watts], TERM_SEQUENCE)

    def make_outputs_verbose(self):
        self._send_to_device("G0", TERM_SEQUENCE)

    def make_outputs_unverbose(self):
        self._send_to_device("G1", TERM_SEQUENCE)
