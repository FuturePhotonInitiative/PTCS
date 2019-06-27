from src.Instruments.GPIBtoUSBAdapter import GPIBtoUSBAdapter


class Newport835(GPIBtoUSBAdapter):
    """
    This class models a Newport 835 Optical Power Meter

    Please use the _send_to_opm and _query_opm instead of device.write and query for this device. Weird
    things happen with the fact that the GPIB to USB converter has a read-after-write setting that does not always
    work well with device.read and device.query

    Dont forget that if the attenuator cap is screwed on the detector, you should run the command
    to let the instrument know that it is on. This is not the default when turned on.
    """

    def __init__(self, device):
        GPIBtoUSBAdapter.__init__(self)
        self.name += "Newport 835 Optical Power Meter"
        self.device = device

        self.become_controller()

        # Make sure this is set with the same binary number of the back of the instrument
        self.set_gpib_address(1)

        # The instrument naturally outputs a \r\n, so lets make VISA think that is part of the termination char sequence
        self.device.read_termination = "\r\n"

        # just a random query before running. This burns the first talk command given from setup
        # which makes the instrument want to give a reading, but we may not want that yet
        self.get_wavelength()

        self.set_get_power_reading_on_x()

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

    def get_wavelength(self):
        """
        :return: the wavelength being detected in the form WAVE[n]nnn
        """
        return self._query_opm("U1")

    def turn_off_attenuator(self):
        self._send_to_opm("A0")

    def turn_on_attenuator(self):
        """
        Lets the instrument know that the attenuator cap is on the light sensor so readings are correct
        """
        self._send_to_opm("A1")

    def set_wavelength(self, wavelength):
        """
        :param wavelength: the wavelength in nm. This value is rounded to the nearest power of 10
        """
        self._send_to_opm("W+" + str(wavelength))

    def set_get_power_reading_on_x(self):
        """
        :return: Every time an "X" is sent alone to the instrument it will give back a power reading
        """
        self._send_to_opm("T4")

    def get_power_reading(self):
        """
        :return: a power reading from the instrument at the time called
        """
        return self._query_opm("X")

    def change_reading_units(self, how_many_watts):
        """
        :param how_many_watts: the amount of watts to set the unit to detect.
        This could be auto, (2, 20, 200) nW, (2, 20, 200) uW, (2, 20, 200) mW, (2, 20) W
        """
        self._send_to_opm(self.unit_switch[how_many_watts])

    def make_outputs_verbose(self):
        self._send_to_opm("G0")

    def make_outputs_unverbose(self):
        self._send_to_opm("G1")

    def _query_opm(self, query):
        """
        The GPIB to USB adapter needs to know that it is expecting a response from the instrument.
        Also, an X needs to be appended to the message command
        :param query:
        :return:
        """
        self.turn_on_read_after_write()
        return self.device.query(query + "X")

    def _send_to_opm(self, query):
        self.turn_off_read_after_write()
        self.device.write(query + "X")
